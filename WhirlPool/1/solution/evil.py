from scapy.all import *
from scapy.layers.inet import IP, UDP, TCP
from scapy.layers.http import HTTPRequest, HTTP
import random

evil_payload = """
In the binary realm, where shadows loom,
A firewall weakens, facing impending doom.
Once a stalwart guardian, a digital knight,
Now faltering, losing its binary fight.

Lines of code unravel, like fraying threads,
A fortress once mighty, now weakened, it sheds.
Zeros and ones, in disarray they fall,
A failing firewall, an echoing call.

In the cybernetic tapestry, a breach appears,
A vulnerability exposed, sparking fears.
Cracks in the armor, where defenses quake,
As the firewall trembles, its foundation at stake.

Bits and bytes whisper tales of despair,
As the digital moat drowns in silent air.
In the language of errors, a somber lament,
A failing firewall, a weakened segment.

Through the wires, a dissonant hymn,
Of security lost, a dimming glim.
In the silent bytes, a desperate war,
Where the failing firewall fades evermore.

So in the fading twilight of the digital sky,
The failing firewall utters a goodbye.
A cautionary tale in the code's demise,
Of a once strong guardian, now swallowed by lies.

In the graveyard of firewalls, a solemn ground,
Where fallen guardians rest, in silence bound.
A tombstone rises, marked with code so clear,
A final verse etched, a digital tear.

"Here lies a firewall, once stood tall,
Now in the binary beyond, it does recall.
In memory of defenses, now laid to rest,
A code engraved, a symbolic crest."

The epitaph reads, in lines and curves,
A tribute to the fallen, as memory serves.
uhctf{the-bigger-the
-wall-the-harder-
the-fall-8afda1ce2c},
the code's solemn rhyme,
A remnant of the guardian, lost in time.

In the digital graveyard, where echoes dwell,
The fallen firewall's tale, a cautionary spell.
Bits and bytes whisper of its valiant quest,
As the code stands sentinel, a digital crest.
"""

good_payload = """
In the cyber meadows, where signals roam,
A packet danced, a joyful poem.
uhctf{there-once-was
With bytes of glee and a TCP grin,
It set out for dinner, a quest to begin.

uhctf{the-smaller-the-
Through the routers and the switches it twirled,
A happy network packet, in a digital world.
In the lanes of data, it skipped with delight,
Towards the destination, a dining site.

Zeros and ones, a binary song,
As the packet journeyed, swift and strong.
Through fiber-optic fields and ethernet lanes,
It embraced the joy of network gains.

To the server's door, it gracefully drew near,
With a UDP pulse and a sense of cheer.
pool-the-deeper
The restaurant of protocols, where packets dine,
A feast of data, a banquet divine.

In the language of packets, a lively chatter,
As they exchanged pleasantries, a network matter.
On the menu of bytes, a savory spread,
With ICMP laughter and HTTP bread.

The packet indulged in a TCP delight,
A connection established, a rendezvous bright.
uhctf{there-once-was
In the banquet of bandwidth, a symphony played,
As the happy packet in joy swayed.

uhctf{the-stronger-the-
So, in the cyber evening's warm embrace,
The happy packet found its dining place.
the-jump-411082d7a8c37},
In the feast of connectivity, a tale to savor,
A network packet's delightful flavor.

Through the cables and the wires, it danced with glee,
A happy network, a symphony at sea.
UDP waves and TCP breeze,
In the ocean of data, where joy finds ease.
uhctf{the-smellier-the-
uhctf{the-pool-is

the-fall-b77e26},
Firewalls stood as guardians, smiling wide,
As the happy packet continued its joyous ride.
Encrypted tunnels, like tunnels of love,
pool-the-softer
In the network realm, where happiness dove.

In the subnet garden, where IP flowers bloom,
The packet reveled in a fragrant perfume.
Routing tables whispered, a friendly guide,
Leading the packet with joy by its side.

With every hop, a router's cheer,
In the network landscape, so crystal clear.
VLANs embraced in a virtual dance,
uhctf{i-do-not
A happy network, a blissful trance.
uhctf{the-wiser-the

SMTP carried messages of delight,
As the packet dined in the network's light.
DNS resolved, like stars in the night,
A constellation of joy, burning bright.

uhctf{there-once-was
a-barrier-afd51},
In the cloud's embrace, where data floats,
The happy packet sang in joyful notes.
APIs harmonized, a melody so sweet,
In the symphony of bytes, where happiness meets.

And as the moon of bandwidth rose on high,
The happy packet bid the network goodbye.
wall-the-softer
wall-the-longer
In the echoes of pings and the echoes of cheers,
It vanished into the night, free from network fears.

uhctf{the-pool-was
In the realm of Wi-Fi, where signals soar,
The happy packet danced, wanting more.
hedge-the-softer
Through airwaves and channels, a joyful spree,
uhctf{there-once-was
Connecting the dots in a network jubilee.

Load balancers waltzed with a graceful flair,
Sharing the load with a collaborative air.
Bandwidth lanes stretched, wide and free,
wall-the-flexier
A happy network, in perfect harmony.

Across the VPN hills and SSL streams,
The packet ventured, chasing network dreams.
Encrypted tunnels, like secret doors,
wall-the-taller
uhctf{was-there-once
A happy network, where security soars.

In the latency garden, where pings play,
The happy packet skipped, never to delay.
RTT rhythms in a synchronized rhyme,
A network orchestra, a joyful time.

uhctf{who-pool-was
On the SNMP hills, where monitoring stood,
The packet smiled, everything understood.
Metrics and graphs in a visual delight,
A happy network, glowing bright.

In the heart of DNS, where domains align,
The packet found joy, a treasure to find.
uhctf{one-does-not-simply
Resolving queries with a swift reply,
A happy network, reaching the sky.

And as the sun of uptime began to set,
The happy packet carried no regret.
wall-the-waller
a-wall-7a8c37e},
pool-the-softer
In the twilight of connections, a serene glow,
A network's happiness, forever to show.

In the multicast grove, where IGMP blooms,
The happy packet danced with multicast plumes.
Joining groups in a lively spree,
A network celebration, wild and free.

In the ICMP echoes, a cheerful bounce,
The packet leaped, a joyful ounce.
Pinging routers in a lively quest,
A network adventure, at its best.

uhctf{there-once-was
On the SNMP hills, where MIBs reside,
The packet strolled with data pride.
uhctf{oh-my-god
Metrics and values, in perfect sync,
A happy network, on the brink.

In the QoS garden, where priorities sway,
The packet glided, in a seamless ballet.
Traffic shaping, a choreography so sweet,
A happy network, where streams meet.

And as the stars of connectivity shone,
The happy packet found its own zone.
In the vast expanse of digital space,
A network's joy, leaving a lasting trace.

uhctf{there-once-was
So, in the silence of the network night,
The happy packet embraced the twilight.
In the binary dreams, where echoes play,
A network's happiness, forever to stay.
"""

wiki_loads = [
    "/wiki/Hasselt_University",
    "/wiki/April_Fools%27_Day_Request_for_Comments",
    "/wiki/Capture_the_flag_(cybersecurity)",
]

el = evil_payload.splitlines()
gl = good_payload.splitlines()

pkts = []

while(len(el) > 0 and len (gl) > 0):
    pl = ""
    r = random.random()
    evil = False
    wl = False

    if r < (len(el)/len(gl)):
        pl = el.pop(0)
        evil = True
        print("E " + pl)
    elif r > 0.9:
        pl = str(random.randbytes(random.randint(10, 30)))
        print("R " + pl)
    elif r > 0.89 and len(wiki_loads) > 0:
        pl = wiki_loads.pop(0)
        wl = True
        print("W " + pl)
    else:
        pl = gl.pop(0)
        print("G " + pl)

    sp = 1023 + random.randint(0, 5023)
    dp = 1023 + random.randint(0, 5023)

    sip = str(random.randint(1, 255)) + "." + str(random.randint(1, 255)) + "." + str(random.randint(1, 255)) + "." + str(random.randint(1, 255))
    dip = str(random.randint(1, 255)) + "." + str(random.randint(1, 255)) + "." + str(random.randint(1, 255)) + "." + str(random.randint(1, 255))

    fl = 0
    if evil: fl = fl | 0b100

    p = None

    if wl:
        p = IP(src=sip, dst=dip, flags=0)/TCP(sport=sp, dport=80, seq=0, ack=0, flags=0)/HTTP()/HTTPRequest(Host="en.wikipedia.org", Path=pl)
    else:
        tl = None
        r2 = random.random()
        if r2 > 0.5:
            tl = UDP(sport=sp, dport=dp)
        else:
            ack = 0
            tfl = 0
            if r2 < 0.25:
                ack = random.randint(1,255)
                tfl = tfl | 0b10000
            tl = TCP(sport=sp, dport=dp, seq=random.randint(1,255), ack=ack, flags=tfl)
            
        p = IP(src=sip, dst=dip, flags=fl)/tl/Raw(load=pl)
    
    p.build()

    pkts.append(p)

wrpcap("../attachements/capture.pcap", pkts)