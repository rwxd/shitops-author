import random


def get_random_words(count: int | None = None) -> list[str]:
    if not count:
        count = random.randint(3, 8)
    random_words = words.split('\n')
    if count > len(random_words):
        raise ValueError(f'only {len(random_words)} words available')
    return random.sample(random_words, count)


words = '''blockchain
kubernetes
service mesh
fast
speed
concurrent
quantum
javascript
typescript
go
python
rust
linux
windows
windows server
redhat enterprise linux
centos
nixos
macos
iphone
android
spotify
music
video
streaming
data
storage
big data
data warehouse
wiki
blog
github
git
gitlab
borg
backup
terrabyte
petabyte
cloudflare
loadbalancing
loadbalancer
berlin
hamburg
london
los angeles
san francisco
apple
microsoft
netflix
network
switch
router
decentralized
technology
reliable
storage
solution
database
mysql
mariadb
oracledb
postgresql
sql
crypto
hashing
security
firewall
algorithm
milliseconds
seconds
api
fastapi
django
flask
scalability
cloud
computing
industrial
iot
website
react
flutter
mobile
platform
time
synchronization
engineering
tech
microservice
microservices
optimization
office
server
cooling
spam
tape
drives
email
snmp
imap
bgp
ospf
e-books
headphones
routing protocol
cumulus linux
cisco
juniper
amazon
aws
azure
ai
chatgpt
2023
2022
2021
2020
2019
2018
2017
2016
outsourcing
gpu
cpu
memory
serverless
lambda functions
mesh
wlan
wifi
datacenter
hybrid
arch linux
checkpoint gaia
fortinet firewall
nvidia
amd
arm chip
raspberry pi
casio
casio g-shock
beer
coffee
money
bank
kindle
vegan
books
lamp
hardware
software
uno
flowers
plants
traffic
traefik
nginx
apache
dns
dhcp
rsync
ssh
ftp
sftp
http
https
let's encrypt
certificates
virtual reality
playstation
xbox
mac mini
macbook
dell
lenovo
thinkpad
quantum computer
rocket
blazingly fast
encryption
openssl
ssl
tls
pokemon
nintendo
gameboy
nintendo ds
twitter
bot
chatbot
machine learning
airpods
airpods pro
germany
usa
australia
europe
world
football
sport
samsung
fridge
smarthome
burger
fries
electricity
fabric
istio
vmware
hyper-v
kvm
sony
jurassic park
avengers
marvel
ipad
television
protocol
tesla
tablets
windows 8
windows 10
windows 11
windows xp
steam
gopro
temperature
blackberry
google maps
apple maps
cinema
whatsapp
signal
telegram
threema
windows phone
salary
recruiting
open telemetry
telemetry
digital twin
nft
bitcoin
ethereum
dogecoin
generative ai
web3
web4
observability
architecture
cybersecurity
neural networks
text-to-speech
speech-to-text
autonomous vehicles
data science
peer-to-peer
nfc
internet tv
biochips
brain-computer interface
5G
4G
3G
virtual assistant
edge computing
micro data center
drones
solid-state-drives
apple watch
bring your own device
natural language processing
space
satellites
mqtt
kafka
sms
icinga2
monitoring
envoy
prometheus
alertmanager
grafana
docker
podman
container
dockerhub
harbor
china
star wars
star trek
game of thrones
hackernews
climate
server
esxi
ocaml
haskell
metallb
cifs
ntp
sshfs
bottleneck
api
rest api
rsa
ed25519
elliptic curve cryptography
business
kibana
logging
logstash
elasticsearch
auto-scaling
cache
redis
world of warcraft
minecraft
fortnite
mobile gaming
mobile apps
camera
search engine
compiler
interpreter
translator
printer
finance
event-driven
websocket
trpc
grpc
site reliability engineering
reliable
1970
4000 bc
1999
2100
mars
moon
saturn
astronaut
netbox
nmap
tcp
udp
wireshark
ethernet
ieee
gitops
minio
s3
gnu hurd
gentoo
ebpf
gnmi
bgp
cilium
fingerprinting
s3fs
xmpp
x11
wayland
sway
matrix
tesla
mac os x
PKI
open source
infrastructure as code
saas
discord
quic
noops
low code
no code
'''
