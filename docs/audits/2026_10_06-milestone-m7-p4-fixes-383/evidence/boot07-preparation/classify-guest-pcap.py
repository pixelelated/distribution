"""Bounded network proof; private actual captures stay outside Git.

IPv6 option/routing header lengths follow RFC8200 sections4.3/4.4/4.6:
https://www.rfc-editor.org/rfc/rfc8200.html
Unsupported/fragmented traffic refuses qualification rather than being skipped.
"""
from pathlib import Path
import collections, datetime, hashlib, json, socket, struct, sys

p=Path(sys.argv[1]);output=Path(sys.argv[2]);raw=p.read_bytes()
assert len(raw)>=24 and raw[:4] in (b'\xd4\xc3\xb2\xa1',b'\xa1\xb2\xc3\xd4')
endian='<' if raw[:4]==b'\xd4\xc3\xb2\xa1' else '>'
assert struct.unpack(endian+'I',raw[20:24])[0]==1,'Ethernet required'
offset=24;count=outbound=positive=0;web=[];queries=[];times=[]
guest_mac=bytes.fromhex('525400524e5b');extensions=collections.Counter();protocols=collections.Counter();icmp6=collections.Counter()
while offset<len(raw):
    assert offset+16<=len(raw),'truncated packet header'
    sec,usec,n,original=struct.unpack(endian+'IIII',raw[offset:offset+16]);offset+=16
    assert offset+n<=len(raw) and n==original,'truncated packet content'
    frame=raw[offset:offset+n];offset+=n;count+=1;times.append(sec+usec/1e6)
    assert len(frame)>=14,'truncated Ethernet frame'
    if frame[6:12]!=guest_mac:continue
    outbound+=1;ether=struct.unpack('!H',frame[12:14])[0]
    if ether==0x0806:continue  # ARP carries no IP transport.
    ip=frame[14:]
    if ether==0x0800:
        assert len(ip)>=20 and ip[0]>>4==4,'invalid IPv4 header'
        ihl=(ip[0]&15)*4;total=struct.unpack('!H',ip[2:4])[0]
        assert 20<=ihl<=total<=len(ip),'invalid IPv4 lengths'
        assert not struct.unpack('!H',ip[6:8])[0]&0x3fff,'IPv4 fragment requires reassembly'
        proto=ip[9];destination=socket.inet_ntop(socket.AF_INET,ip[16:20]);payload=ip[ihl:total]
        assert proto in (1,2,6,17),'unsupported IPv4 protocol'
    elif ether==0x86dd:
        assert len(ip)>=40 and ip[0]>>4==6,'invalid IPv6 header'
        size=struct.unpack('!H',ip[4:6])[0]
        assert size and 40+size<=len(ip),'invalid/unsupported IPv6 payload length'
        proto=ip[6];destination=socket.inet_ntop(socket.AF_INET6,ip[24:40]);payload=ip[40:40+size]
        chain=0
        while proto in (0,43,60):
            assert chain<8 and len(payload)>=8,'truncated/overlong IPv6 extension chain'
            assert proto!=0 or chain==0,'Hop-by-Hop must be first'
            length=(payload[1]+1)*8
            assert length<=len(payload),'truncated IPv6 extension body'
            extensions[str(proto)]+=1;proto,payload=payload[0],payload[length:];chain+=1
        assert proto in (6,17,58,59),'fragmented or unsupported IPv6 next header'
        if proto==58:
            assert len(payload)>=4,'truncated ICMPv6'
            icmp6[str(payload[0])]+=1
    else:
        raise AssertionError('unsupported outbound EtherType '+hex(ether))
    protocols[str(proto)]+=1
    if proto==6:
        assert len(payload)>=20,'truncated TCP header'
        header_size=(payload[12]>>4)*4
        assert 20<=header_size<=len(payload),'invalid TCP header length'
        source_port,dest_port=struct.unpack('!HH',payload[:4]);data=payload[header_size:]
        if dest_port in (80,443):web.append(dict(destination=destination,port=dest_port,protocol='tcp',seconds=sec+usec/1e6))
        if dest_port==9045 and b'GET /pixelelated-network-positive-control HTTP/' in data:positive+=1
    if proto==17:
        assert len(payload)>=8,'truncated UDP header'
        source_port,dest_port,length,_=struct.unpack('!HHHH',payload[:8])
        assert 8<=length<=len(payload),'invalid UDP length'
        if dest_port in (80,443):web.append(dict(destination=destination,port=dest_port,protocol='udp',seconds=sec+usec/1e6))
        if dest_port==53:
            dns=payload[8:length];assert len(dns)>=12,'truncated DNS header'
            if dns[2]&0x80:continue
            assert struct.unpack('!H',dns[4:6])[0]==1,'unsupported DNS question count'
            pos=12;labels=[]
            while True:
                assert pos<len(dns),'truncated DNS label'
                size=dns[pos];pos+=1
                if size==0:break
                assert size<64 and pos+size<=len(dns),'unclassified DNS question'
                labels.append(dns[pos:pos+size].decode('ascii'));pos+=size
            assert pos+4<=len(dns),'truncated DNS question type'
            queries.append('.'.join(labels).lower())
blocked_dns=[q for q in queries if any(x in q for x in ['github','rocknix','rasteratops','pixelelated'])]
report=dict(observed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),pcap_sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw),packets=count,outbound_packets=outbound,capture_seconds=times[-1]-times[0] if times else 0,positive_control_requests=positive,outbound_web_packets=web,dns_questions=queries,upstream_dns_queries=blocked_dns,ipv6_extensions=dict(extensions),transport_protocols=dict(protocols),icmpv6_types=dict(icmp6),passed=bool(count and outbound and positive and not web and not blocked_dns),scope='Bounded startup/forced-update/CLI capture; no TCP/UDP80/443 or named upstream/project DNS requests. Local9045 positive required. Unsupported or fragmented traffic refuses proof; not a claim of all-protocol silence.')
output.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2));assert report['passed'],'guest network capture failed its bounded predicate'
