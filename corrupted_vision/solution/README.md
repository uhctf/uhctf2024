# Solution
The blob in the URL is AES/CBC encrypted data (cipher text). More specifically, your user ID and user name. The description hints at the number 0, i.e. the "admin" user ID (as most systems, we don't care about names). We can manipulate the cipher text without the key by simply changing the bytes.
We don't have to brute force all possible values, though. Tampering with the encrypted bytes can be done in a controlled manner, despite not knowing the key. This is because we can see the what is inside the encrypted data (plain text) on the webpage. This is done as follows:
1. base64 decode the cipher text. Note that this is URL-safe base64 data, which uses a slightly different character set from default base64
2. tamper with 1 random byte in the decoded data
3. base64 encode it back, and put it in the URL
4. observe what changed. Repeat the above till you know which encrypted byte corresponds with which user name character or user ID number
5. determine the exact tampered byte value to use to get your desired output. This can be done by abusing XOR's commutative property:
    1.  get current cipher text byte value (= `a`)
    2.  get byte value shown on screen (= `b`)
    3.  get desired character byte value (= `c`)
    4.  XOR them together (`a ^ b ^ c`) to get the byte value that you can put in the cipher text
6. repeat the focused tampering. Remember, the goal is setting the user ID to 0. `BZVdTPhc2o71W1ouMvGLWa5AALHimHTR1BY8lBmk1ss` should be a solution.