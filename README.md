# Tail Time
Tail Time is a website fingerprinting defense built on top of Walkie-Talkie. In Tail Time, communication between the client and the server is done in half-duplex except for that an active request cannot block queued requests longer than the configured timeout value. Additionally, the cell sequences of website traces are padded using a reference trace to ensure similarity between different websites.
## Trace Collection
Clone the [tor-capture](https://github.com/csmcguan/tor-capture) repository and move the provided extensions in ./tail-time/addon to ./tor-capture/visit/addon. Follow the instructions for setup and trace capture provided in the README. After collecting traces, move the ./tor-capture/log to ./tail-time.
## Padding
Padding can be applied to all configurations for which there are traces by the following command.
```
sh sim.sh
```
Padding can also be applied to individual configurations with the following command.
```
sh sim.sh <config>
```
## Overhead
Bandwidth and latency overhead can be calculated for all configurations for which there are traces by the following command. The output will be logged to the files bwoh.txt and loh.txt.
### Bandwidth Overhead
```
sh bwoh.sh
```
### Latency Overhead
```
sh loh.sh
```
The overhead can also be calculated for individual configurations with the following command. The output is displayed to the screen.
### Bandwidth Overhead
```
sh bwoh.sh <config>
```
### Latency Overhead
```
sh loh.sh <config>
```
## Reference
J. Liang, C. Yu, K. Suh and H. Han, "Tail Time Defense Against Website Fingerprinting Attacks," in IEEE Access, vol. 10, pp. 18516-18525, 2022, doi: [10.1109/ACCESS.2022.3146236](https://doi.org/10.1109/ACCESS.2022.3146236).
