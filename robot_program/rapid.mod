MODULE Module1
    !***********************************************************
    !
    ! Module:  Module1
    !
    ! Description:
    !   <Insert description here>
    !
    ! Author: KRDOKIM13
    !
    ! Version: 1.0
    !
    !***********************************************************


    !***********************************************************
    !
    ! Procedure main
    !
    !   This is the entry point of your program
    !
    !***********************************************************
    PERS num val_pc{6}:=[0,0,0,0,0,0];
    PERS num nPos{6}:=[0,0,0,0,0,0];


    CONST robtarget pRobHome:=[[125.832194166,450.28522019,338.677970192],[0.106285491,0.715957957,0.128961155,0.677847047],[0,-1,0,4],[138.371807265,9E+09,9E+09,9E+09,9E+09,9E+09]];
    PERS robtarget pRobTest:=[[125.832,589.785,329.178],[0.106285,0.715958,0.128961,0.677847],[0,-1,0,4],[138.372,9E+9,9E+9,9E+9,9E+9,9E+9]];

    VAR string tempOut:="";
    VAR string tempIn:="";
    VAR string parse:="";
    VAR iodev OutFile;
    VAR iodev inFile;
    VAR bool flag;
    PERS num val;

    PROC main()

        !MoveAbsJ [[0,0,0,0,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]]\NoEOffs,v1000,fine,tool0;
        MoveJ pRobHome,v1000,fine,tool0\WObj:=wobj0;
        rReset;
        !TeachTarget:=CRobT(\Tool:=tool0\WObj:=wobj0);
        !AccSet 10,10;

        WHILE diExternal=0 DO
            WaitUntil val_pc{1}<>0 OR val_pc{2}<>0 OR val_pc{3}<>0 OR diOpen<>0 OR diClose<>0;
            IF diOpen=1 THEN
                !External Input set to 1 = Gripper Open
                SetDO doClosed,0;
                WaitTime(0.1);
                SetDO doOpened,1;
                tempOut:=ValToStr(1);
                Write OutFile,tempOut;
                tempOut:="";
            ELSEIF diClose=1 THEN
                !External Input set to 0 = Gripper Closed
                SetDO doOpened,0;
                WaitTime(0.1);
                SetDO doClosed,1;
                tempOut:=ValToStr(0);
                Write OutFile,tempOut;
                tempOut:="";
            ELSE
                !nPos:=[nPos{1}+val_pc{1},nPos{2}+val_pc{2},nPos{3}+val_pc{3},nPos{4}+val_pc{4},nPos{5}+val_pc{5},nPos{6}+val_pc{6}];
                pRobTest:=Offs(pRobHome,val_pc{1},val_pc{2},val_pc{3});
                MoveJ pRobTest,v3000,z50,tool0\WObj:=wobj0;
                tempOut:=ValToStr(pRobTest.trans);
                Write OutFile,tempOut;
                tempOut:="";
            ENDIF
            val_pc:=[0,0,0,0,0,0];

        ENDWHILE
        
        IF diExternal=1 THEN
            Close InFile;
            tempIn:="";
            Open "HOME:/path.txt",InFile\Read;
            WaitTime(0.1);
            
            
            WHILE tempIn<>EOF DO
            tempIn:=ReadStr(InFile\RemoveCR);
            parse:=StrPart(tempIn,1,StrLen(tempIn));
            IF StrLen(tempIn)>1 THEN
                flag:=StrToVal(parse,pRobTest.trans);
                MoveJ pRobTest,v500,z10,tool0\WObj:=wobj0;
            ELSEIF StrLen(tempIn)=1 THEN
                flag:=StrToVal(parse,val);
                IF val=1 THEN
                    SetDO doClosed,0;
                    WaitTime(0.1);
                    SetDO doOpened,1;
                    WaitTime 2;
                ELSE
                    SetDO doOpened,0;
                    WaitTime(0.1);
                    SetDO doClosed,1;
                    WaitTime 2;
                ENDIF
            ELSE
                !Error Message
            ENDIF
        ENDWHILE
        ENDIF

    ENDPROC


    PROC rReset()
        nPos:=[0,0,0,0,0,0];
        val_pc:=[0,0,0,0,0,0];
        SetDO doClosed,0;
        SetDO doOpened,0;
        WaitTime(0.5);
        SetDO doClosed,1;

        IF diExternal=0 THEN
            Close OutFile;
            Open "HOME:/path.txt",OutFile\Write;
            waittime(0.1);
        ENDIF

    ENDPROC

ENDMODULE
