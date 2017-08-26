### Comments

(TODO)

- 這道題目用到的密碼學，主要是 [block cipher][bc] 和 [block cipher mode of
  operation][mo] 當中的 CBC mode。

- 觀察 prob.py 程式數個可被利用的弱點：

  1.  server 用 CBC 模式加密訊息時，使用的 IV 是固定的
  2.  server 解密訊息後要做的 unpad() 並不會 reject 那些 padding 格式錯誤的訊息
  3.  server 沒有使用 [MAC][mac]，密文沒有 authenticity
  4.  `send_msg('Welcome!!')` 和 `send_msg('')` 和 `send_msg('command not found')` 和 `send_msg(flag)` 會送給我們這四組明文密文 pairs，提供了許多微調 IV 去 replay 做 chosen ciphertext attack 的空間
  5.  只要一個 block 的 byte 0、byte 1、byte 2 已知，我們就可以利用 `echo` 指令
      1.  做 chosen ciphertext attack 去猜一個 block 加密前的 byte 15
      2.  做 chosen ciphertext attack 去猜一個 block 加密前的 byte 3 到 byte 14，一次只猜一個 byte
  6.  利用 `echo` 指令，可以讓第二個 block 的 byte 0、byte 1、byte 2、byte 3 被 shift 進第一個 block

- 其實就算 prob.py 檔案 while True 無窮迴圈中，十多行的 if-elif-...-else
  程式被化簡到只剩下兩個 cases 像這樣子：

      if msg.startswith('exit'):
          exit(0)
      else:
          send_msg('command not found')

  我們也可以輕鬆地找出 flag 的明文。

- 這道題目的答案是 `hitcon{IV_15_ve3y_funny}`

- 不太一樣但蠻相關的 [padding oracle attack][poa] 十分經典，這些看似很傻的弱點有不少實際案例

### If you want to run your own problem server...

With the prob.py script, you can easily run your own instance of the problem
server:

    $ dd if=/dev/urandom count=1 bs=16 2> /dev/null > key.txt
    $ echo "hitcon{$( dd if=/dev/urandom count=1 bs=256 2> /dev/null | LC_ALL=C tr -d -c 'a-zA-Z0-9_' | head -c 16 )}" > flag.txt
    $ python2.7 -m pip install pycrypto
    $ netcat -k -l -p 12345 -c 'python2.7 prob.py'


[mac]: https://en.wikipedia.org/wiki/Message_authentication_code
[bc]: https://en.wikipedia.org/wiki/Block_cipher
[mo]: https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation
[poa]: https://en.wikipedia.org/wiki/Padding_oracle_attack