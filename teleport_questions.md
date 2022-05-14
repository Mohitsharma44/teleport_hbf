- **How would you prove the code is correct?**

  While I didn't get enough time to flush out proper unit testing and end to end testing in the couple of days that I got to spend with the implementation, one can run `make test` which will spawn the hbf container along with a bunch of httpd containers listening on ports 8101 - 8109. The e2e script also tries to make get requests to this endpoint and fails after 5 successive requests (set by `HBF_MAX_PORTS` environment variable) in less than `HBF_TIME_THRESHOLD`.

  For automated testing, one can run:
  ```
    sudo make e2e-test
  ``` 

  You should see the following log lines from hbf container:
  ```
    [+] Running 1/1
    ⠿ Container teleport-test-hbf-1  Recreated                                                                                                                0.1s
    Attaching to teleport-test-hbf-1
    teleport-test-hbf-1  | A rudimentary Host Based Firewall using BPF and XDP
    teleport-test-hbf-1  | In file included from <built-in>:2:
    teleport-test-hbf-1  | In file included from /virtual/include/bcc/bpf.h:12:
    teleport-test-hbf-1  | In file included from include/linux/types.h:6:
    teleport-test-hbf-1  | In file included from include/uapi/linux/types.h:14:
    teleport-test-hbf-1  | In file included from include/uapi/linux/posix_types.h:5:
    teleport-test-hbf-1  | In file included from include/linux/stddef.h:5:
    teleport-test-hbf-1  | In file included from include/uapi/linux/stddef.h:5:
    teleport-test-hbf-1  | In file included from include/linux/compiler_types.h:76:
    teleport-test-hbf-1  | include/linux/compiler-clang.h:35:9: warning: '__HAVE_BUILTIN_BSWAP32__' macro redefined [-Wmacro-redefined]
    teleport-test-hbf-1  | #define __HAVE_BUILTIN_BSWAP32__
    teleport-test-hbf-1  |         ^
    teleport-test-hbf-1  | <command line>:4:9: note: previous definition is here
    teleport-test-hbf-1  | #define __HAVE_BUILTIN_BSWAP32__ 1
    teleport-test-hbf-1  |         ^
    teleport-test-hbf-1  | In file included from <built-in>:2:
    teleport-test-hbf-1  | In file included from /virtual/include/bcc/bpf.h:12:
    teleport-test-hbf-1  | In file included from include/linux/types.h:6:
    teleport-test-hbf-1  | In file included from include/uapi/linux/types.h:14:
    teleport-test-hbf-1  | In file included from include/uapi/linux/posix_types.h:5:
    teleport-test-hbf-1  | In file included from include/linux/stddef.h:5:
    teleport-test-hbf-1  | In file included from include/uapi/linux/stddef.h:5:
    teleport-test-hbf-1  | In file included from include/linux/compiler_types.h:76:
    teleport-test-hbf-1  | include/linux/compiler-clang.h:36:9: warning: '__HAVE_BUILTIN_BSWAP64__' macro redefined [-Wmacro-redefined]
    teleport-test-hbf-1  | #define __HAVE_BUILTIN_BSWAP64__
    teleport-test-hbf-1  |         ^
    teleport-test-hbf-1  | <command line>:5:9: note: previous definition is here
    teleport-test-hbf-1  | #define __HAVE_BUILTIN_BSWAP64__ 1
    teleport-test-hbf-1  |         ^
    teleport-test-hbf-1  | In file included from <built-in>:2:
    teleport-test-hbf-1  | In file included from /virtual/include/bcc/bpf.h:12:
    teleport-test-hbf-1  | In file included from include/linux/types.h:6:
    teleport-test-hbf-1  | In file included from include/uapi/linux/types.h:14:
    teleport-test-hbf-1  | In file included from include/uapi/linux/posix_types.h:5:
    teleport-test-hbf-1  | In file included from include/linux/stddef.h:5:
    teleport-test-hbf-1  | In file included from include/uapi/linux/stddef.h:5:
    teleport-test-hbf-1  | In file included from include/linux/compiler_types.h:76:
    teleport-test-hbf-1  | include/linux/compiler-clang.h:37:9: warning: '__HAVE_BUILTIN_BSWAP16__' macro redefined [-Wmacro-redefined]
    teleport-test-hbf-1  | #define __HAVE_BUILTIN_BSWAP16__
    teleport-test-hbf-1  |         ^
    teleport-test-hbf-1  | <command line>:3:9: note: previous definition is here
    teleport-test-hbf-1  | #define __HAVE_BUILTIN_BSWAP16__ 1
    teleport-test-hbf-1  |         ^
    teleport-test-hbf-1  | 3 warnings generated.
    teleport-test-hbf-1  | 2022-05-10 07:07 HBF   DEBUG    Loading existing blocklist ips


    teleport-test-hbf-1  | 2022-05-10 07:09 HBF   DEBUG    Rapid connections have been detected from 172.16.178.1 to port 8001
    teleport-test-hbf-1  | 2022-05-10 07:09 HBF   DEBUG    Rapid connections have been detected from 172.16.178.1 to port 8002
    teleport-test-hbf-1  | 2022-05-10 07:09 HBF   DEBUG    Rapid connections have been detected from 172.16.178.1 to port 8003
    teleport-test-hbf-1  | 2022-05-10 07:09 HBF   DEBUG    Rapid connections have been detected from 172.16.178.1 to port 8004
    teleport-test-hbf-1  | 2022-05-10 07:09 HBF   DEBUG    Rapid connections have been detected from 172.16.178.1 to port 8005
    teleport-test-hbf-1  | 2022-05-10 07:09 HBF   DEBUG    Port Scanning detected from 172.16.178.1
    teleport-test-hbf-1  | 2022-05-10 07:09 HBF   INFO     Blocked 172.16.178.1
  ```

  For a bit more manual testing, one can run:

  ```
    # Install HBF
    sudo make install
    # Start HBF
    sudo test_teleport_hbf start

    # Start httpd containers
    for i in {1..9}; do docker run -d --name web{i} -p 810{i}:80 httpd > /dev/null 2>&1; done

    # Start making some curl requests
    for i in {1..9}; do echo "=== 800$i ==="; curl -s -I -m 1 <ip>:810$i; sleep 0.1; done
    ```
    In hbf logs, you should see something like:
    ```
    2022-05-10 02:48 HBF          DEBUG    Loading existing blocklist ips
    2022-05-10 02:48 HBF          DEBUG    Rapid connections have been detected from 172.16.178.1
    2022-05-10 02:48 HBF          DEBUG    Rapid connections have been detected from 172.16.178.1
    2022-05-10 02:48 HBF          DEBUG    Rapid connections have been detected from 172.16.178.1
    2022-05-10 02:48 HBF          DEBUG    Rapid connections have been detected from 172.16.178.1
    2022-05-10 02:48 HBF          DEBUG    Rapid connections have been detected from 172.16.178.1
    2022-05-10 02:48 HBF          DEBUG    Port Scanning detected from 172.16.178.1
    2022-05-10 02:48 HBF          INFO     Blocked 172.16.178.1
  ```

* **How would you make this solution better?**

  Quite a few things actually.
  - Re-arch to have a data plane/ controller plane (daemon/ client) type of model.
  - Output in a more human and machine processable format. Currently, I'm simply logging to console and logfile. I'd like to implement something like a json output
  - Add more metrics.
  - Have the ips list be accessible from multiple sources instead of just files (like query external db)
  - Improve cli piece to be able to add/ remove ips from the blocklist
  - If we must run HBF in containers, I'd like to improve the arch such that we can run multiple bpf programs/ filters on single interface (maybe explore libxdp and migrate the code to that).
  - Improve the testing piece

* **Is it possible for this program to miss a connection?**
  - If you mean is it possible for a few port scan traffic to pass? 
    Yes, my implementation of HBF sends the connection information to the userland process which then performs checks for port scans. If identified, it adds the ip to blocklist which then bpf program reads the list (well, map in my case) and based on that it blocks the connection. Until the decision to block the connection is made, its possible to pass a few hits from port scan depending on how rapid the scan is.

* **If you weren't following these requirements, how would you solve the problem of logging every new connection?**
  - This is a near realtime solution. I don't think packet processing can get faster than the BPF implementations. Sure, maybe hardware offloading could improve speed but we're definitely able to log every connection.

* **Why did you choose x to write the build automation?**
  I've used Makefile and docker. Makefiles are ubiquitous in most tools and fairly easy to implement. Honestly, never thought of trying to look into alternatives since it does everything I want it to.
  docker is industry standard and when it comes to containerization technology. I'm a mac user so I initially thought of writing nerdctl and use containerd using colima but that would've added another layer of complexity for testing. Instead, I decided to use vagrant to give me a linux OS in VM and have docker build container images in it.

* **Is there anything else you would test if you had more time?**
  Currently, we dont have proper unit tests for the bpf program in C or even python code. So thats what I would focus some time on.

* **What is the most important tool, script, or technique you have for solving problems in production? Explain why this tool/script/technique is the most important.**
  Not sure if there is ONE tool to rule them all kind of thing. Different problems require different tools. 
  - If I'm investigating a problem, I look at the logs. So something like kibana if we're using elk stack.
  - I guess after that, based on my troubleshooting technique, the first thing I do is try and log in to the host and check the system's state so maybe df, (h)top, free, du are quite important for me.
  - If its a networking issue, depending on the nature, I go to ip, ping, nslookup, dig, nc etc.
  - If its something where I need to track down a process, ps, pstree, strace, ptrace etc.
  By this point, there is something that generally pops out.
  If we are talking about technique then I believe very strongly in service ownership. If a different team has written a service that has some problems in production, I would strongly advocate adding member of that team to the troubleshooting as soon as possible. They are the SMEs for their service. Ofcourse, once you gain enough experience with the service, you can troubleshoot alone but its a slippery slope that I try to avoid. 

* **If you had to deploy this program to hundreds of servers, what would be your preferred method? Why?**
  - If the program was to be deployed to hundreds of servers (and has been re architected to my above suggestion), I would bake the HBF program in the AMI (or the OS image equivalent in other cloud/ on prem environments) using tool like packer if possible. If not, then resort to ansible to make a pristine image that will be used as base OS.
  - There will be a DB that would store a list of blocklisted IPs and the infrastructure to manage all of that will be handled using infrastructure as a code tool like terraform.
  - There would be different accounts/ environments where the changes to HBF will be tested in (with at least one mimicking the cust/ prod environment). The rollout to prod, depending on the security policy, should be as touchless as possible. Meaning a change graduates from Dev environment -> gets tested in staging (integration tests/ functional tests) -> moves to NPRD (or cust like environment) where it gets tested against a subset of customer traffic (or entirely mirrored) and if things look good to developers -> Optional push of button for approval -> Gets rolled out to CUST environment in a Blue Green or Canary fashion.

* **What is the hardest technical problem or outage you've had to solve in your career? Explain what made it so difficult?**
  There are 2 that come to mind. One from current work and one from a consulting job.
  *Background*:
  Up until a year or so ago we were managing our AWS infrastructure using terraform locally from our laptops. Meaning the deploys to cust environments (and a few others) were performed from Ops's laptops and Devs were free to make changes to the play environments. 
  *Issue*:
  Things were fine initially when had fewer accounts to manage each running a few resources until we grew to more than 30 accounts with even more environments in each and in all using over 1K resources. This meant the terraform deploys were taking forever to complete and our laptops were pinned at 100% CPU (running plans for nprocs - 1 environments in parallel) rendering it almost unusable for anything else.
  *Challenge*: 
  We wanted to come up with an auditable, one click deploy solution that requires approval before final rollout and something that won't hog our system resources.
  *Proposal*:
  There were quite a few solutions like atlantis, codedeploy pipelines, using jenkins, custom tooling that would spawn ecs tasks that performs the deploys etc. We chose to proceed with codedeploy pipelines (it will be quite a long response if I were to mention the pros and cons of each and why we chose codedeploy pipelines but I'm happy to chat in person).
  The reason why the implementation was challenging was because of all the different moving pieces that we had to design. The architecture had to be such that it doesn't cause any friction in developers development cycle. Ensure that the pipeline cannot be used to bypass any security practice at workday (especially when ecs tasks were assuming cross account roles for execution). It had to be scalable and has to respect the geopolitical restrictions. In the event of failure, it has to rollback the service to the previous working release.
  (Unfortunately, this is the most I can disclose but more than happy to chat in detail later).

  Since I cannot share much technical detail about the above process, I can share another technical problem that I feel proud of solving. This was a few years ago in my previous job. 
  *Background*:
  I was working with Urban Observatory at NYU CUSP. The small research group had received a grant to pursue research in trying to understand the dynamics of the urban cities. The PI was able to secure funds to purchase some computing resources. 
  *Issue*:
  The problem was that there were a few researchers who wanted access to those compute environments and run their analysis on. Unfortunately, the research project only had 2 compute nodes each with 256 GB RAM and 56 Cores of CPU (in total). The research scientists wanted an isolated environment to be able to install the tools they need, modify the environment the way they want and have data from their analysis persist.
  As you can imagine, giving ssh access with root priviledges is not an option. Another option was virtualization but sharing ballooning memory across bunch of VMs wouldn't have kept them happy. 
  *Solution*:
  I designed "dockkeeper", a container based system for researchers to have their own compute environments that would run on these baremetals as containers giving them complete root access in their containers (but using namespace remapping so that root in container does not equal root on the underlying system). So had to design all kinds of authentication integrations to work with this.
  Another interesting challenge I ran into was, since I was using docker swarm for orchestration (kubernetes was still heavily in development and had breaking changes almost every other release not to mention the installation was not so straightforward at that time) was that whenever there was a network outage or power interruption or any hiccup that would cause the containers to restart, the data persisted since I was using bind volumes for their home dirs and other mount points but they would lose things that were "installed in the environment" because these tools/ applications were added to the read-only container fs. I implemented a snapshot system that would take a just in time snapshot of the container every hour, tar gzip the file and whenever there was an outage, dockkeeper would reload these environments from these "snapshot" (this was way before CRIU, checkpoint/restore in userspace had support for docker. Fun times!).
  I still work on this probono occasionally adding more features when possible but I've changed the architecture significantly now that the research team has acquired more funds and are in multiple geographical locations.
