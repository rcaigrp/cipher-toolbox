# Hunt Queries for llama.cpp RPC Servers

These queries help identify potentially exposed llama.cpp RPC servers on your network.

## Splunk SPL

```
| inputlookup known_hosts | where host IN (list of hosts to check)
| exec cmd="netstat -tuln | grep 50052" | regex "0\.0\.0\.0:50052"
```

## Microsoft KQL (Azure Sentinel, etc.)

```
// Check for processes listening on port 50052
ProcessEvents
| where ProcessCommandLine contains "50052"
| project Timestamp, HostName, ProcessCommandLine, ProcessId
```

## Plain grep/jq

```bash
# Check for processes using port 50052
netstat -tuln | grep 50052

# Alternative: check for llama.cpp processes with RPC enabled
ps aux | grep llama.cpp | grep 50052
```

## YARA Hunt

```bash
yara -r /path/to/detection/yara/llama_cpp_rpc_server.yar /opt /usr/local
```