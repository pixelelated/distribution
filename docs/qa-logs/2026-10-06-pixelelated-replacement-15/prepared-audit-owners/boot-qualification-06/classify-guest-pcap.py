"""Classify a closed, owned QEMU Ethernet capture; retain all packet counts."""
from pathlib import Path
import datetime,hashlib,json,socket,struct,sys
p=Path(sys.argv[1]);output=Path(sys.argv[2]);raw=p.read_bytes()
assert raw[:4] in (b'\xd4\xc3\xb2\xa1',b'\xa1\xb2\xc3\xd4')
endian='<' if raw[:4]==b'\xd4\xc3\xb2\xa1' else '>'
assert struct.unpack(endian+'I',raw[20:24])[0]==1,'Ethernet link type required'
offset=24;count=outbound=positive=0;web=[];queries=[];times=[];guest_mac=bytes.fromhex('525400524e5b')
while offset<len(raw):
 assert offset+16<=len(raw),'truncated packet header'
 sec,usec,n,original=struct.unpack(endian+'IIII',raw[offset:offset+16]);offset+=16
 assert offset+n<=len(raw) and n==original,'truncated packet content'
 frame=raw[offset:offset+n];offset+=n;count+=1;times.append(sec+usec/1e6)
 if len(frame)<14 or frame[6:12]!=guest_mac:continue
 outbound+=1;ether=struct.unpack('!H',frame[12:14])[0]
 if ether==0x0800:
  ip=frame[14:];assert len(ip)>=20;ihl=(ip[0]&15)*4;proto=ip[9];destination=socket.inet_ntop(socket.AF_INET,ip[16:20]);payload=ip[ihl:]
 elif ether==0x86dd:
  ip=frame[14:];assert len(ip)>=40;proto=ip[6];destination=socket.inet_ntop(socket.AF_INET6,ip[24:40]);payload=ip[40:]
  # Unknown extension chains cannot establish no-web evidence.
  assert proto not in (0,43,44,50,51,60),'unclassified IPv6 extension chain'
 else:continue
 if proto==6 and len(payload)>=20:
  source_port,dest_port=struct.unpack('!HH',payload[:4]);data=payload[(payload[12]>>4)*4:]
  if dest_port in (80,443):web.append({'destination':destination,'port':dest_port,'seconds':sec+usec/1e6})
  if dest_port==9045 and b'GET /pixelelated-network-positive-control HTTP/' in data:positive+=1
 if proto==17 and len(payload)>=20 and struct.unpack('!H',payload[2:4])[0]==53:
  dns=payload[8:]
  if dns[2]&0x80:continue
  pos=12;labels=[]
  while pos<len(dns) and dns[pos]:
   size=dns[pos];assert size<64 and pos+1+size<=len(dns),'unclassified DNS question';labels.append(dns[pos+1:pos+1+size].decode('ascii'));pos+=1+size
  queries.append('.'.join(labels).lower())
blocked_dns=[q for q in queries if any(x in q for x in ['github','rocknix','rasteratops'])]
report={'observed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pcap_sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),'packets':count,'outbound_packets':outbound,'capture_seconds':times[-1]-times[0] if times else 0,'positive_control_requests':positive,'outbound_web_packets':web,'dns_questions':queries,'upstream_dns_queries':blocked_dns,'passed':bool(count and outbound and positive and not web and not blocked_dns),'scope':'bounded guest startup/forced-update/CLI observation; no HTTP80/TLS443 packets or upstream-host DNS queries during this capture; local9045 positive control required, no claim of all-protocol silence'}
output.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2));assert report['passed'],'guest network capture failed its bounded predicate'
