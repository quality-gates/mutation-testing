# Mutation Testing

Mutation testing is a way to make your automated tests more reliable. You make small changes to your code (mutants) and if your automated tests fail as a result, then that's a mutant kill. If your tests pass, that's a mutant escape. 

The general idea is that a mutant escape is bad, because your tests didn't notice that a line of your code change. Now, not all mutants are equal in value. If you change the output of a console log, then you could argue your tests don't really need to detect that. If a user wouldn't see critical behaviour fail or change as a result of that mutated bit of code, then that's an equivalent mutant. 

But the important bit here isn't terminology. The important bit is **code changed -> automated tests caught it by failing** and you can make your own judgement on what specific types of code change you value most. 

Language specific tools essentially build up a big tree of your code and use that to rattle through a great big list of code mutations to try, automatically running your test suite as it goes. It's often slow and intensive but it's extremely valuable in finding testing gaps or even bugs. 

## Automated Tools

Many tools exist for this, and I should plug my own tools here - [mutago](https://github.com/quality-gates/mutago) in particular for Go is the most feature-complete tool even if it's not the most well known, with Go-specific idioms that other mutations testing tools miss.It is also the only mutation tester for Go that includes git-diff-aware mutations and tracks the covered-MSI % metric. It's the perfect regression guard to put into your CI pipeline if you run a Go codebase.  

These automated mutation testing tools expose testing gaps very quickly and in my opinion are the strongest line of defence against AI slop. Claude and other models will write passing tests, but you can never guarantee they'll write effective tests without proper prompting. Even then, I've found, AI-written tests are often tautological, relying on mocks and fakes. They often _can't fail_ and that makes them useless as regression guards. 

Automated mutation testing tools identify test slop with brutal efficiency. They expose which of your tests are actually pulling their weight, no matter what kind of code coverage you have. You could be executing 100% of your code in your tests, but an automated mutation testing tool could show that your tests aren't covering some critical input classes that could actually happen with your application code in prod. 

If you maintain a codebase in any of the major languages, you really can't afford to miss out on mutation testing, especially not in 2026 when nearly ever software developer uses Claude Code or an equivalent. 

## Manual Mutation Testing

But let's step back for a second. Mutation testing doesn't have to be automated. Sometimes your code repo is in a collection of different languages, or you need to run mutation testing at a higher level. You need to see, for example, if mutating a Dockerfile line is detected by your automated tests. And those automated tests could literally be, up Dockerfile as a container and run smoke tests on it. 

Mutation testing requires code to mutate, a build process, and automated tests that can pass or fail. That's it. Conceptually it's something you can do without an automated mutation testing tool. 

Ideally, you get an AI model to do it for you, but carefully prod the model to ensure its list of mutants is complete and somewhat deterministic. Document the test, the results, and use it in successive runs if you want to be thorough. 

## So What? 

AI slop is going to become more of a problem for people maintaining codebases. Mutation testing is a quality gate AND a tool to close out the blind spots in your tests. Automated tools give you a constant quality gate against sloppy code and tests, and manual mutation tests force you to think of _what_ you can mutate to represent genuine behavioural changes.  
