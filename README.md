# DTP-base

This is (meant to be) a tool for digging through the Department for
Transport's brake test database, in order to find a brake test
procedure by DTp number, and some other such stuff.

The database is pre-populated with the November 2020 DTP update,
described thusly:

> The attached files are for updating the vehicle database of ATF RBT's,
> The DVSA have requested that all units are updated by 1st
> November 2021. The update includes new Dtp numbers 9867 to 9958. (9958
> relates to a 3 axle Mercedes Benz rigid 26000kg GVW, Solo parking on
> axle 2&3, with the split service brake as the nominated secondary.)
> Therefore the existence of these additional numbers on your RBT data
> base will confirm if an update has been installed. this file format is
> for VLT units.

At some point, I may make it work such that the database can be
updated with the ministry's DTA files.

# Licensing

## The Database
The contents of the V2101/DTA database are a product of the Department
for Transport, and as such are public sector information licensed
under the Open Government License v3.0.

They are provided 'as-is', with no warranty, and the Department for
Transport are not liable for any errors or omissions.

For full terms, see:
https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/

The .sql files under V2101/ are created by myself as a simple
transformation of the contents of the .dta files, under the terms of
the OGL v3.0.

The DTA-base.sqlite database is produced mechanically from these
files, and is also licensed under the OGL v3.0

## The Code

[Except where otherwise noted, code is provided under the terms of the AGPL v3.0 license, a copy
of which is provided](LICENSE.md)

### _SQL_UTIL.PY
`_sql_util.py` is Copyright 2018 lemon24, provided by the
 [reader project](https://github.com/lemon24/reader), licensed under
 the BSD 3-clause license as below:
 Copyright 2018 lemon24

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

1.  Redistributions of source code must retain the above copyright
    notice, this list of conditions and the following disclaimer.

2.  Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in the
    documentation and/or other materials provided with the distribution.

3.  Neither the name of the copyright holder nor the names of its
    contributors may be used to endorse or promote products derived from
    this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


# FAQ

## Why?

I wanted to try figure out what DTp number my truck might get, when I
finally try to register it, and some idea of what plated weights it
might get assigned.

And then it spiralled from there.

## No, but... Why?

*shrug*

## What the hell is this?

Originally, when statutory annual MOT testing was introduced on heavy
goods vehicles and trailers, back in the **applies rose-tinted
spectacles** halcyon days of 1968 **removes rose-tinted spectacles**,
there was a stack of cards provided with every roller brake tester
that detailed the procedures to be used for brake testing each
specific type of truck.

This was required, because quite frankly the brake systems on trucks
of the day ranged from simple, to the absolute batshit insane.

(Fuck you, Bedford, and your stupid fucking "let's make the park brake
work by making some rollers grip on a shaft, by pressing a tapered
collar around them; and and and, let's make it so that it will apply
the brake if you lose either one of your primary or secondary air
brake feeds!")

Anyway, every time a new type of vehicle was introduced, a new card
would be added to the stack; this, as you can imagine, lead to an
enormous pile of cards (nearly 3000, by 1982.)

This was getting ridiculous! And so, a new start was needed, and thus
we have the Brake Master Database; which lets you do an electronic
lookup of the procedure to brake test every vehicle under the
administrations of the former Ministry of Transport, now the
Department for Transport.
