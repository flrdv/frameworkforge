wrk.method = "POST"
wrk.path = "/"
local body = "Hello, world!"
wrk.headers["Content-Length"] = body.len()
wrk.body = body
