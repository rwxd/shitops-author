import random


def get_random_words(count: int | None = None) -> list[str]:
    if not count:
        count = random.randint(7, 12)
    random_words = [w for w in words.split("\n") if w != ""]
    if count > len(random_words):
        raise ValueError(f"only {len(random_words)} words available")
    return random.sample(random_words, count)


words = """blockchain
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
time sensitive
synchronization
engineering
tech
microservice
optimization
office
cooling
spam
tape
drives
email
snmp
imap
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
multi tenant
message broker
message queue
metaverse
cybersecurity mesh
hyperautomation
sustainable technology
function as a service
platform as a service
golang
evpn
vxlan
ipv6
single pane of glass
network function virtualisation
tdd
agile
agility
scrum
distributed ledger
java
distributed real-time
pubsub
enterprise service bus
responsive design
fintech
10x engineer
unicorn
cloud evangelist
grok
gnu
ecosystem
smart watch
accelerated
extreme programming
homebrew
homegrown
build or buy
gameboy advance
fibre channel
nintendo wii
sap
4k
8k
checkpoint cloudguard
vmware nsx-t
vmware tanzu kubernetes
design
zero-trust
mainframe
mission-critical
compliance
ITIL
adaptive security appliance
cisco firepower
mesh vpn
DevOps
Continuous development
Continuous delivery
Homomorphic encryption
Hyperledger
Explainable artificial intelligence (XAI)
Quantum supremacy
Bioinformatics
Swarm robotics
Neuromorphic computing
Edge intelligence
Ambient intelligence
Biohacking
Cyborg
Federated learning
DNA computing
Augmented reality contact lenses
Swarm intelligence
Haptic technology
Neuroinformatics
Gesture recognition
Wearable technology
Robotic exoskeletons
Nanoengineering
Neurofeedback
Quantum cryptography
QR Code
USB
GPS
Cloud storage
Antivirus
Password
Browser cache
Cookies
E-Commerce
Fitness tracker
online shopping
Self-driving cars
mobile payment
automation
Polymorphism
Binary tree
Debugging
Testing
Agile development
Framework
Profiler
Test-driven development
Regression testing
Integration testing
Unit testing
Algorithm
Recursion
Version control
IDE (Integrated Development Environment)
Functional programming
Event-driven programming
Concurrency
Multithreading
Asynchronous programming
Serialization
Deserialization
JSON (JavaScript Object Notation)
XML (Extensible Markup Language)
Full-stack development
MVC (Model-View-Controller)
ORM (Object-Relational Mapping)
NoSQL
MongoDB
Software development lifecycle
Waterfall model
Agile methodology
Pair programming
CSS (Cascading Style Sheets)
CCNA
CCNP
CCIE
MCIV
Microsoft Excel
Microsoft Word
Microsoft Power Point
C-Level
CEO
CTO
bfd
network engineering
network architecture
OSI model
Intrusion Detection System (IDS)
Intrusion Prevention System (IPS)
VLAN (Virtual Local Area Network)
Latency
Packet loss
Documentation
Software-defined networking (SDN)
Disaster recovery
traffic engineering
configuration management
capacity planning
audits
LibreNMS
helm
Service Level Agreement (SLA)
key performance indicator (kpi)
operational level of agreement (ola)
kanban
cmdb
Rancher
Techradar
webshop
blackbox
cronjob
Extract, transform, and load (ETL)
on call
business continuity plan (BCP)
virtual machine
business intelligence
Slack
Microsoft Teams
F5 Loadbalancer
lab
request for help
request for comment
powerdns
bind
dns resolver
self hosting
cisco anyconnect
Site-2-Site
ISMS
Out of Band
availability
Private VLAN
Ansible
WSL
Renewable energy
Green IT
Green technology
Internet of Medical Things (IoMT)
3D printing
Hyperloop transportation
Space tourism
Dark matter exploration
Cyber-physical systems
Intelligent transportation systems
Smart grids
turing award
nobel prize
certificate renewal
tensorflow
hadoop
numpy
dotnet
angular
vue
skype
internet explorer
stateful
stateless
DynamoDB
Cassandra
deadline
PhD
internship
overtime
Postdoc
team event
workshop
power point presentation
"""
