#include <uapi/linux/bpf.h>
#include <uapi/linux/if_ether.h>
#include <uapi/linux/ip.h>
#include <uapi/linux/tcp.h>
#include <uapi/linux/in.h>

// We're using BPF ringbuffer. This feature was addedd in Linux kernel 5.8.
// Make sure your kernel version is >= 5.8
BPF_RINGBUF_OUTPUT(callers, 8);
BPF_HASH(blocklist, u32);

struct connInfo {
  u32 destPort;
  u32 sourceIP;
};

int packetwatch(struct xdp_md *ctx) {

  // Obtain pointer to data from XDP struct
  void *data = (void *)(long)ctx->data;
  void *data_end = (void *)(long)ctx->data_end;

  // Check if the ethernet frame is valid
  struct ethhdr *eth = data;
  if (eth + 1 > (struct ethhdr *)data_end)
  {
    return XDP_DROP;
  }

  // We're only working with ipv4
  struct iphdr *iph = NULL;
  iph = (data + sizeof(struct ethhdr));
  if (iph + 1 > (struct iphdr *)data_end) {
    return XDP_DROP;
  }

  struct tcphdr *tcph = NULL;
  struct udphdr *udph = NULL;
  struct icmphdr *icmph = NULL;
  struct connInfo retVal = {};
  
  // Filtering based on different protocols
  switch (iph->protocol)
  {
    // We'll only look at TCP for now
    case IPPROTO_TCP:
      tcph = (data + sizeof(struct ethhdr) + (iph->ihl * 4));
      if (tcph + 1 > (struct tcphdr *)data_end) {
        // Malformed TCP packet
        return XDP_DROP;
      }
      // Drop some well known attacks
      if (tcph->fin == 1 && tcph->psh == 1 && tcph->urg == 1)
      {
        // XMAS scan
        return XDP_DROP;
      }
      if (tcph->fin == 1 && tcph->cwr == 0 && tcph->ece == 0 && tcph->urg == 0 && tcph->ack == 0 && tcph->psh == 0 && tcph->rst == 0 && tcph->syn == 0)
      {
        // FIN scan
        return XDP_DROP;
      }
      if (tcph->fin == 0 && tcph->cwr == 0 && tcph->ece == 0 && tcph->urg == 0 && tcph->ack == 0 && tcph->psh == 0 && tcph->rst == 0 && tcph->syn == 0)
      {
        // NULL scan
        return XDP_DROP;
      }

      int key = iph->saddr;
      if (blocklist.lookup(&key)) {
        return XDP_DROP;
      }
      
      if (!(tcph->syn) || (tcph->ack)) {
        retVal.destPort = tcph->dest;
        retVal.sourceIP = iph->saddr;
        callers.ringbuf_output(&retVal, sizeof(retVal), 0);
      }
      return XDP_PASS;
    // ToDo
    // case IPPROTO_UDP:
    //   // Sanity check on udp header length.
    //   udph = (data + sizeof(struct ethhdr) + (iph->ihl * 4));
    //   if (udph + 1 > (struct udphdr *)data_end)
    //   {
    //     return XDP_DROP;
    //   }
    //   return XDP_PASS;

    // case IPPROTO_ICMP:
    //   // Sanity check on ICMP header length
    //   icmph = (data + sizeof(struct ethhdr) + (iph->ihl * 4));
    //   if (icmph + 1 > (struct icmphdr *)data_end)
    //   {
    //     return XDP_DROP;
    //   }
    // return XDP_PASS;
  }
  return XDP_PASS;
}