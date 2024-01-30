# Framework Forge

## Motivation
There are many benchmarks existing, **and none of them is correct**. Neither does this, because its purpose
is not to demonstrate, how fast frameworks will work on the simple hello world and/or adding big latencies
syntactically. This is just not representative: the more latency there is, the less contribution of the framework.
So, we're basically measuring how well __the language__ can hang in I/O. For example, adding 500ms latency already
erases any overhead by framework, so it basically makes no sense.

However, we do benchmark the **bare framework overhead**. Databases aren't the part of it. So what we do, is checking
edge cases like:
- Bare GET request
- Simple Hello-world POST request
- Huge request with a veeery long request line and a lot of headers
- Colossal body in POST request

So by that, we can see the overhead of the framework by itself. No matter what happens in business logic, **if you're
already looking at benchmarks - it must be fast enough to gain from web-framework switching**.

## Approach
Benchmark target must be a complete web-application, which uses the specified framework. It must neither be a
production-ready code nor simply 'hello world', but something in the middle. The application must have multiple
endpoints, that'll be introduced later.

You're allowed to:
- disable non-essential middlewares (e.g. logger, panic handler)
- use more performant settings preset if provided by the framework
- enable pre-forking

You're forbidden to:
- use the framework in the different way than the community usually does. This includes undocumented API and various hacks
- tune the framework manually
  * if not explicitly allowed
- use more performant tooling instead of built-in (e.g. using custom JSON encoder/decoder)
  * if not explicitly allowed

## How tests are running?
Each framework, found in the directory `frameworks/<language>`, is being started in a separated process. We're requesting 
the homepage until getting a response, indicating the readiness. Then, we're running `wrk` tool in another process (in
order to obtain the wrk's output). We're running it multiple times, using every time the next script from the `cases/` 
directory. Each script represents some benchmark case, and can be easily extended (however, on this mechanism I'm still
working). 

## Pros
The stand (we) aims to provide the highly flexible, extensible and configurable platform. Maybe, once I'll even
introduce a web-gui and similar to hardware benchmarks feature, where everyone can run the benchmarks on own machine
and submit results to be visible publicly. Who knows, who knows