wrk.method = "POST"
wrk.path = "/"
local body = "Hello, world!"
wrk.headers["Content-Length"] = string.len(body)
wrk.body = body
