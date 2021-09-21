CREATE TABLE IF NOT EXISTS Master
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
        FoundServBrake        	      INT,
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

CREATE TABLE IF NOT EXISTS TrailerWeights
 (
        NrAxles                       INT,
        GVWDesign                     INT,
        Axle1Weight                   INT,
        Axle2Weight                   INT,
        Axle3Weight                   INT,
        Axle4Weight                   INT,
        Axle5Weight                   INT,
        Dummy                 	INT,
        TotalAxleWeight               INT,
        DTpNumber                     Text (14)
);

CREATE TABLE IF NOT EXISTS VehMake
 (
        MakeId                INT NOT NULL,
        Make                  Text (100) NOT NULL
);

CREATE TABLE IF NOT EXISTS VehType
 (
        TypeId                Text (6) NOT NULL,
        Type                  Text (100) NOT NULL
);

CREATE TABLE IF NOT EXISTS Version
 (
        Version                   Text (20),
        "Date of update"          DateTime
);
