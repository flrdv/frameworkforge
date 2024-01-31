# Framework Forge

## Motivation
**There are many benchmarks, and none of them is correct. So neither does this one.**

The more delay in user code, the less contribution of the framework into the overall performance. So by that, there
won't be tests of CRUD or any other kind of applications, that are IO-bound. Instead, what we're testing here is the
pure performance of web-frameworks.

Almost always, the web-framework doesn't matter, if the user-code executes for too long. For example, 500ms of delay
already levels almost any of toolchain's cost. But if you do want to switch to another instrument, thus looking
benchmarks, your business logic must be already fast enough to gain from the switching. In this case, more interesting
would be to look at how different libraries handle with different edge-cases. No matter whether it's a simple GET,
file distribution, huge HTTP request or the request, that causes the application to respond with an error.

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
and submit results to be visible publicly. Who knows, who knows.
