# llb3d

llb3d - LLVM Blitz3d implementation

## License

            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
                    Version 2, December 2004

 Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>

 Everyone is permitted to copy and distribute verbatim or modified
 copies of this license document, and changing it is allowed as long
 as the name is changed.

            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

  0. You just DO WHAT THE FUCK YOU WANT TO.

## Language

Language parser implement by [PLY](http://www.dabeaz.com/ply/).

    Copyright notice.

    Next sections has copied from [Blitz Docpack](http://www.blitzbasic.com/).

### Keywords

The following keywords are built into Blitz, and may not be used as
identifiers (variables, function names, labels, etc.):

    After, And, Before, Case, Const, Data, Default, Delete, Dim, Each, Else,
    ElseIf, End, EndIf, Exit, False, Field, First, Float, For, Forever,
    Function, Global, Gosub, Goto, If, Insert, Int, Last, Local, Mod, New,
    Next, Not, Null, Or, Pi, Read, Repeat, Restore, Return, Sar, Select, Shl,
    Shr, Step, Str, Then, To, True, Type, Until, Wend, While, Xor, Include

### Comments

You add comments to your programs using the ';' character.
Everything following the ';' until the end of the line will be ignored,
this is useful for commenting your code - so you can always look through and
follow each line in a logical manner.

- The following code shows comments in use;


    ; Begin the Redraw Function
    Function Redraw()
    ...
    End Function

- This code also shows a legal use of comments;


    Function Redraw() ; Begin the Redraw Function
    ...
    End Function

### Identifiers

Identifiers are used for constant names, variable names, array names,
function names and custom type names.

Identifiers must start with an alphabetic character, and may be following
be any number of alphanumeric characters, or the underscore `_` character.

    RE: [_a-z]\w+

These are all valid identifiers:

- `Hello`
- `Score`
- `player1`
- `time_to_live`
- `t__`

Indentifiers are not case sensitive.

For example, `Test`, `TEST` and `test` are all the same identifiers.

However, it is allowed for identifiers to be reused for functions and
custom types names.

For example, you can have a variable called `test`, a function called `test`
and custom type name called `test`. Blitz will be able to tell which one you
are refering to by the context in which it is used.

### Basic Data Types

There are 3 basic data types:

- Integer values are numeric values with no fractional part in them.
  For example: `5`, `-10`, `0` are integer values. All integer values in your
  program must be in the range `-2147483648` to `+2147483647` (`int32`).

- Floating point values are numeric values that include a fractional part.
  For example: `.5`, `-10.1`, `0.0` are all floating point values (`float32`).

- Strings values are used to contain text. For example: `"Hello"`,
  `"What's up?"`, `"***** GAME OVER *****"`, `""`.

Typically, integer values are faster than floating point values, which are
themselves faster than strings.

### Constants

Constants may be of any basic data type.
Constants are variables that have fixed values that will not change (ever)
during the course of your program. These are useful tools for things like
screen resolution variables, etc.

Floating point constants must include a decimal point, for example:

    '5' is an integer constant, but '5.0' is a floating point constant.

String constants must be surrounded by quotation marks, for example:

    "This is a string constant".

The 'Const' keyword is used to assign an identifier to a constant. For example:

    Const width = 640, height = 480

You can then use the more readable 'width' and 'height' throughout your
program instead of `640` and `480`.

Also, if you ever decide to change the width and height values,
you only have to do so at one place in the program.

There are two built-in Integer constants - `true` and `false`.
`true` is equal to `1`, and `false` is equal to `0`.

There is also a built in floating point constant for `Pi`.
