#include <stdlib.h>\n#include <unistd.h>\nint main() { int x = rand(); char buf[10]; getrandom(buf, 10, 0); return 0; }
