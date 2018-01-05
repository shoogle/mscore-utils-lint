[mscore-utils-lint]
===================

[mscore-utils-lint]: https://github.com/shoogle/mscore-utils-lint "mscore-utils-lint upstream code repository"

Placeholder repository for static analysis tool for [MuseScore].

[MuseScore]: https://musescore.org/ "MuseScore sheet music editor"

Check for common mistakes and bad-practise in scores,
and for compliance with the [OpenScore] [guidelines].

[OpenScore]: https://openscore.cc/ "OpenScore sheet music digitization project"
[guidelines]: https://musescore.com/shoogle/scores/3434266 "OpenScore guidelines"

Inspired by Debian/lintian.

## Not an XML/MSCX syntax checker

[mscore-utils-lint] checks *valid* MuseScore files for usage patterns that are discouraged,
for whatever reason, despite being valid MSCX syntax.

## Plan

Currently the repository only contains the issues (or "flags") that the program will check for,
not the code to check for them.
This is because we have yet to decide on the best way to implement the program.

The choices are:

- In [MuseScore]'s C++ code
  - PROS:
    - easy for users to run
    - easiest way to stay up-to-date with MuseScore's MSCX syntax
  - CONS:
    - harder to program in C++ than other languages
    - hardest to update. Must update MuseScore to update the linter.
    - increases size of MuseScore binary
- Via MuseScore QML plugin
  - PROS:
    - easy to run
    - fairly easy to update
    - independent of changes to MSCX syntax
  - CONS:
    - limited syntax and command line support
    - limited to score information exposed by MuseScore's plugin API
    - plugin API might change
- Python
  - PROS:
    - easily extensible
    - can become part of mscore-utils
    - Python parser already done in mscore-utils-join
    - could be put on webserver - anyone can visit webpage and upload a score
  - CONS:
    - difficult for non-developers to run locally
    - can break with changes to MSCX syntax
- JavaScript
  - PROS:
    - anyone can visit a webpage and upload a score
  - CONS:
    - no existing MSCX parser
    - can break with changes to MSCX syntax

It is hoped that building up the list of tags will help make this decision.

### YAML tag syntax

```yaml
# flags.yml
---
Flag: text-has-manual-formatting
Severity: normal # major, normal, minor, wishlist
Certainty: certain # certain, probable, possible, guess
Info: >-
  Don't manually format text (e.g. as bold or italic) if you
  can use a text style such as "Technique" instead. You can
  create a new style if none of the existing ones are suitable.
Ref: https://musescore.com/shoogle/scores/3434266
Help: https://musescore.org/en/handbook/text-styles-and-properties
---
# next flag
```
