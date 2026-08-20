# 1) Keep V0's TCP/socket structure
#    NO CHANGE

# 2) Receive request as bytes
#    V0: decode while receiving
#    V1: keep bytes → decode only when parsing

# 3) Parse HTTP
#    V0: METHOD PATH VERSION
#    V1: METHOD PATH VERSION + HEADERS

# 4) Validate requests
#    NEW: malformed request → 400
#    NEW: unsupported HTTP version → reject

# 5) Handle paths
#    V0: "/" → "/index.html"
#    V1: separate path from "?query"
#    NEW: URL decoding
#    KEEP: traversal protection

# 6) Content-Type
#    V0: always text/html
#    V1: determine from file extension

# 7) Responses
#    KEEP: 200 / 403 / 404 / 405
#    IMPROVE: correct headers/content types

# 8) Testing
#    NEW: use your own client to send controlled requests