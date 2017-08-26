以下劇透本題解答。

如果您還沒解題、且想要自行體會解謎樂趣，請趕快回上一頁。


---


### Comments and Our Solutions

(TODO)

- 這道題目需要用到的密碼學知識：

  1. [block cipher][bc]
  2. [block cipher mode of operation][mo] 當中的 CBC mode

- 觀察 prob.py 程式之特性與可被利用的弱點：

  1.  server 用 CBC 模式加密訊息時，使用的 IV 是固定的
  2.  server 解密訊息後要做的 unpad() 並不會 reject 那些 padding 格式錯誤的訊息
  3.  server 沒有使用 [MAC][mac]，密文沒有 authenticity
  4.  `send_msg('Welcome!!')` 和 `send_msg('')` 和 `send_msg('command not found')` 和 `send_msg(flag)` 會送給我們這四組明文密文 pairs，提供了許多微調 IV 去 replay 做 chosen ciphertext attack 的空間
  5.  只要一個 block 的 byte 0、byte 1、byte 2 已知，我們就可以利用 `echo` 指令
      1.  做 chosen ciphertext attack 去猜一個 block 加密前的 byte 15
          - 猜 byte 15 的值
          - 調整 IV 使得明文 prefix 是 'echo' 且明文 byte 15 值是 12
          - 觀察結果是 `send_msg('')` 就是猜中 byte 15 了，否則就是猜錯了
          - 猜錯了，就再猜一個別的值
      2.  做 chosen ciphertext attack 去猜一個 block 加密前的 byte 3 到 byte 14，一次只猜一個 byte
          - 猜 byte i 的值
          - 調整 IV 使得明文 prefix 是 (' '*(i-3) + 'echo') 且明文最後一個 byte 值是 (15-i)
          - 觀察結果是 `send_msg('command not found')` (猜錯) 還是 `send_msg('')` (猜中了)
          - 猜錯了，就再猜一個別的值
  6.  利用 `echo` 指令，可以讓第二個 block 的 byte 0、byte 1、byte 2、byte 3 被 shift 進第一個 block

- 其實，就算 prob.py 檔案 while True 無窮迴圈中，十多行的 if-elif-...-else
  程式被化簡到沒有 echo 等指令了，只剩下兩個 cases 這樣子：

      if msg.startswith('exit'):
          exit(0)
      else:
          send_msg('command not found')

  我們也一樣可以找出 flag 完整的明文。重點是這個 oracle 讓我們能夠區分 chosen
  ciphertext 被解密以後對應到的明文的兩種 cases...  這就直接洩漏了明文關於某一個 byte 的資訊了。

- 和 TCP server 互動的輔助程式: [utils.py](utils.py)

- 建議寫點程式自動化

- 這道題目的答案是 `hitcon{IV_15_ve3y_funny}`

- 不太一樣但蠻相關的 [padding oracle attack][poa] 十分經典，這些看似很傻的弱點有不少實際案例


---


### If you want to run your own problem server...

With the prob.py script, you can easily run your own instance of the problem
server:

    $ dd if=/dev/urandom count=1 bs=16 2> /dev/null > key.txt
    $ echo "hitcon{$( dd if=/dev/urandom count=1 bs=256 2> /dev/null | LC_ALL=C tr -dc a-zA-Z0-9_ | head -c 16 )}" > flag.txt
    $ python2.7 -m pip install pycrypto
    $ netcat -k -l -p 12345 -c 'python2.7 prob.py'


[mac]: https://en.wikipedia.org/wiki/Message_authentication_code
[bc]: https://en.wikipedia.org/wiki/Block_cipher
[mo]: https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation
[poa]: https://en.wikipedia.org/wiki/Padding_oracle_attack
