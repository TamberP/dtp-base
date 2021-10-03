# DTp Database

The DTp database contains data required to properly perform a roller
brake-test on a HGV. For full technical details and a lot less sarcasm, please see:

[https://www.gea.co.uk/wp-content/uploads/2015/11/624.pdf]

## The DTp number

Identifies a complete vehicle braking system, and is core to looking
up the correct RBT procedure. It is generally given on the vehicle's
VTG-6.

Vehicles manufactured prior to the introduction of type-approval have
a 4 character numeric, possibly followed by a single alpha character
(A to E).

Post type-approval, the Dtp numbers start from 3000 and are all
four-character numeric. Where one of these vehicles has been modified
after manufacture, these numbers are identified by a 'B' prefix.

### Suffixes

These identify differing brake characteristics within the same basic
vehicle type. These suffixes will not appear on the vehicle plate, but
they are in the database to allow for variance.

They indicate that there is some sort of option, related to the brake
system, that must be identified by the person performing the brake
test. e.g. whether the vehicle has been fitted with a park brake on
the first axle or not.

* F: Unused
* G: Drum brakes or Disc brakes?
* H: Two or three position hand-control fitted?
* I: Park brake on Axles 1&4, 2&4, or 2&3?
* J: Type 24 or Twinstop 12/30 actuators on front axle?
* K: Park brake on axle 1?
* L: Secondary & park brake on axle 1?
* M: Park brake on axle 2?
* N: Secondary and park brake on axle 3?
* O: Park brake on axles 1&2, 1&3, or 2 only?
* P: Secondary & parking brakes on axle 4?
* Q: Unused
* R: Unused
* S: Second alternative when options are available
* T: Used as the third option when option I is used
* U: Used as the third option when option O is used.
* V to Z: Unused

## Vehicle Make

A three character numeric code that identifies the vehicle make; this
is then looked up in the appropriate database table to return a
human-readable vehicle make/manufacturer.

## Vehicle Type

A two character alphanumeric code that identifies the vehicle type:
How many axles does it have? Is it a rigid, or a tractor-unit, or a
trailer?

## Pre/Prior/Post 1968 Options

A single-character field identifying whether the vehicle should be
tested under pre-1968 or post-1968 brake performance requirements.

If yes, then the vehicle tester would then be asked what brake
standards to test the vehicle to. As you may guess, pre-1968 is a lot
less strict.

### Service Brake Performance Requirements

For all other than 'pre-1968' vehicles, the total service brake
performance requirement is 50% of the Design Gross Vehicle Weight.

For pre-1968, it varies by the number of axles, whether the vehicle is
a rigid or a tractor unit... oh, and also, pre-1968 vehicles aren't
required to have a brake on every axle. Enjoy that thought!

### Secondary Brake Performance Requirements

There are two types of secondary brake: A completely separate system
with a hand-lever in the cab (Old school), or a split service brake
system where both halves of the split are completely independent
systems operated by the single foot-operated service brake pedal.

For the majority of vehicles, the total secondary brake performance
requirement is: 25% of the Design Gross Vehicle Weight.

For pre-1968 vehicles... *sigh* it varies with the number of axles and
whether the vehicle is a rigid or a tractor unit.

'Prior-1968' and 'post-1968' tractor unit vehicles must meet 25% of
the Gross **Train** Weight, if the secondary brake does not operate on
the trailer.

### Optional Systems

If the designated secondary brake system doesn't meet the performance
requirements, then the efficiency of another brake system (as long as
it can be applied separately) make be taken into account as an
alternative!

e.g. if either one half of a split braking system, or a separate
secondary system, failed to achieve the requirement, but another
*progressively* (that word is important. It must be, they bolted it in
the spec.) applied brake does achieve the requirements, then you have
met the requirement.

### Parking Brake

There are no specific requirements for 'pre-1968' vehicles. As long as
it doesn't roll away in the test-lane, and you meet the general
"little or no brake effort" minimum standard of 5% of the axle weight,
per wheel, you're fine.

For type approved vehicles, you must meet the greater of either:
- 16% of the DGVW
- 12% of the GGTW

Fun little diversion: There is a note in the spec about testing
vehicles with transmission brakes. That is, you must test them by
running both wheels on the axle together, in the same direction, and
you *must* chock the front wheels otherwise *YEET*.

I can confirm this.

## Brake Routine

Used to describe what axles are braked under what category, and thus
how to test this vehicle.

In brakrout.dta, this is 4 fields:
* The first, a 3 character alphanumeric code, is used in the
  master.dta database to reference into brakrout.dta. First character:
  What axles does the service brake operate on? Second character: What
  axles does the secondary brake system operate on -- either axle
  details, or a split system. And the third character identifies which
  axles have park brakes.

  - 0: Split system
  - 1: Axle 1
  - 2: Axle 2
  - 3: Axles 1 & 2
  - 4: Axle 3
  - 5: Axles 1 & 3
  - 6: Axles 2 & 3
  - 7: Axles 1, 2, & 3
  - 8: Axle 4
  - 9: Axles 1 & 4
  - A: Axles 2 & 4
  - B: Axles 1, 2, & 4
  - C: Axles 3 & 4
  - D: Axles 1, 3, & 4
  - E: Axles 2, 3, & 4
  - F: Axles 1, 2, 3, & 4

  e.g 754 brake routine would have a service brake operating on axles
  1, 2, and 3; a secondary brake operating on axles 1 and 3; and a
  park brake that operates only on axle 3
* Field 2: As above, but showing the axles on which the service brake
  operates.
* Field 3: Either details -- as above -- on which axles the secondary
  brake operates, **OR** the word 'SPLIT'. Unsurprisingly, SPLIT
  indicates that the vehicle has a split braking system rather than a
  separate secondary system. (Try saying that five times quickly.)
* Field 4: As with field 2, but now describing which axles the park
  brake works on.

Yes, this is kinda repeating itself, but you do have to remember this
format was designed for computers in the mid-80s, and extended along
the way.

## Split Routines

4-character alphanumeric code that identifies which bit of a split
service system is classed as the secondary brake.

This may be a front-rear split, a diagonal split, an 'L' split, an
inner/outer split (axle 1+4, and axle 2+3), or 'duplicate'.

## Second Front Axle Steered

Does the vehicle have one or two *front* steered axles that should be
checked for ovality? (Steering axles that aren't at the front don't
count.)

## Brake Distribution (Service)

Provides, as a percentage, how well the service brake on the front
axles is expected to perform compared to that of the rears. Used when
calculating FWA, when a front wheel locks during the brake test.

A value of '50', on a two-axle vehicle, would mean that both axles
should be expected to provide the same static brake force.

A three axle vehicle with a single front axle, and with identical
brake components on all axles, would reasonably be expected to give
the same performance on all axles and thus this would be 33%.

A three axle vehicle with two steering front axles, and with identical
brake components on all axles (and expected... yadda yadda), would
have 33% of its total brake force generated by each front axle and
this would thus be 66%.

Clear as mud?

## Brake Distribution (Secondary)

Basically the same as for the above, but for the secondary brake
system; with the exception that, where the secondary brake only works
on the front axle (and where you'd expect the distribution to be 100%)
this will be '99' because the format only defines two characters for this.

## Transmission Secondary/Park Brake

Does this vehicle have a transmission park or secondary brake? (If so,
BOO, HISS!)

## Secondary Brake on Tractor Only

Does the tractor unit have secondary brakes that *only* operate on the
unit itself? If not, then it *does* provide secondary braking to the
trailer, and the secondary brake performance is assessed against the
Gross Train Weight rather than the Gross Vehicle Weight.

## Design Gross Vehicle Weight

The maximum Gross Vehicle Weight for this vehicle group. The number is
given as GVW/10, due to limitations in the early format. e.g. 7500kg
is 0750.

## Design Gross Train Weight

Maximum Gross Train Weight for this vehicle group. Format is as for
the Design GVW.

## Design Weight Axle [1, 2, 3, 4]

Provides the maximum design axle weight for the respective axle. Again
given in weight/10 form.

## Method of Operation (Service, Secondary, Park)

Describes what type of brake system the respective brake is; whether
it's mechanical, hydraulic, air, air-over-hydraulic, spring, electric,
etc.

## Load Sensing Valve Fitted, and Load Sensing Valve Option

Does it have a load sensing valve? Or does it have one as an optional
fitment?

## Brake Modulation

Identifies axles that might not give full braking effort unless
loaded, due to having brake pressure modulated by some means of weight
sensing.

## Double Drive Fitted/Third Diff Fitted

If a vehicle is fitted with a double-drive axle and **does not** have
a third differential, things may go **BANG** if the proper procedure
is not followed and the roller brake tester tries to drive one of the
axles, while the other is held still by the ground.

The correct procedure is, then, to test the brakes by rotating the
wheels of that axle in opposite directions. I have never had to do
this. Wanna bet I fuck it up first time, and make a big mess?

## Trailer Numbering System

A system is in place to allow the identification of draw-bar trailers
and semi-trailers, whether single or multi axle, and -- for draw-bar
trailers -- whether it's a full draw-bar or a centre-axle draw-bar.

The code also encodes the Gross Vehicle Weight except where it's a
semi-trailer in which case it encodes a reference into a separate set
of files because semi-trailers make things more complicated.

It *also* encodes whether the trailer has load-sensing valves,
anti-lock brakes, or electronic brake systems. Oh, and whether or not
the trailer is type approved.

The separate set of files list the GVW of the trailer, in ranges of
250kg; design axle weights; total axle weight of the bogie (Which,
when the trailer is coupled, is the GVW minus the weight being
supported by the tractor unit.), and a reference number for the
routine.

## Public Service Vehicle Number System

This encodes:
- Laden weight, or GVW, of the PSV.
- Whether a split braking system is designated as secondary, and if so what type
- Whether a separate designated secondary brake system is fitted
- And what axles the parking brake operates on. Code 'F' here
  indicates a transmission brake is fitted.

# DTA database update file format

(coming soon(TM))

# SQlite3 Schema
CREATE TABLE Master
 (
        DTpNumber                     Text (14) NOT NULL,
        DuplicateID                   Text (2),
        MakeId                        INT,
        TypeId                        Text (4),
        BrakeRoutine                  Text (8),
        PPPSelector                   INT NOT NULL,
        SplitRoutine                  Text (8),
        SecFrontAxleSteered           INT NOT NULL,
        ServiceBrakeDestrib           INT,
        SecBrakeDestrib               INT,
        TransSecParkBrake             INT NOT NULL,
        SecBrakeOnlyOnTrac            INT NOT NULL,
        GVW_DesignWeight              INT,
        GTW_DesignWeight              INT,
        Axle1DesignWeight             INT,
        Axle2DesignWeight             INT,
        Axle3DesignWeight             INT,
        Axle4DesignWeight             INT,
        Axle5DesignWeight             INT,
        ABSFitted                     INT NOT NULL,
        ABSOption                     INT NOT NULL,
        SecParkBrakeOnDiffAxle        INT NOT NULL,
        FoundServBrake                INT,
        FoundSecBrake                 INT,
        FoundParkBrake                INT,
        PosSecBrakeLever              INT,
        LSVFitted                     INT NOT NULL,
        LSVOption                     INT NOT NULL,
        ModAxle1Affect                INT NOT NULL,
        ModAxle2Affect                INT NOT NULL,
        ModAxle3Affect                INT NOT NULL,
        ModAxle4Affect                INT NOT NULL,
        ModAxle5Affect                INT NOT NULL,
        DoubleDriveFitted             INT NOT NULL,
        AskThirdDiffFitted            INT NOT NULL
);
CREATE TABLE TrailerWeights
 (
        NrAxles                       INT,
        GVWDesign                     INT,
        Axle1Weight                   INT,
        Axle2Weight                   INT,
        Axle3Weight                   INT,
        Axle4Weight                   INT,
        Axle5Weight                   INT,
        Dummy                   INT,
        TotalAxleWeight               INT,
        DTpNumber                     Text (14)
);
CREATE TABLE VehMake
 (
        MakeId                INT NOT NULL,
        Make                  Text (100) NOT NULL
);
CREATE TABLE VehType
 (
        TypeId                Text (6) NOT NULL,
        Type                  Text (100) NOT NULL
);

CREATE TABLE BrakType
 (
	TypeId  INT NOT NULL,
	Type    Text(64) NOT NULL
);

CREATE TABLE Version
 (
        Version                   Text (20),
        "Date of update"                DateTime
);
