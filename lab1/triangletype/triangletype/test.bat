
SET program="%1"
if %program% == "" goto err


%program% 1 2 3 4
if not errorlevel 1 goto testFailed


%program% 1 2 
if not errorlevel 1 goto testFailed


%program% 1 2 4 > 1_2_4.txt
if errorlevel 1 goto testFailed
fc /b 1_2_4.txt check/1_2_4.txt
if errorlevel 1 goto testFailed

%program% 2 3 4 > 2_3_4.txt
if errorlevel 1 goto testFailed
fc /b 2_3_4.txt check/2_3_4.txt
if errorlevel 1 goto testFailed

%program% 5 5 5 > 5_5_5.txt
if errorlevel 1 goto testFailed
fc /b 5_5_5.txt check/5_5_5.txt
if errorlevel 1 goto testFailed

%program% 78 65 78 > 78_65_78.txt
if errorlevel 1 goto testFailed
fc /b 78_65_78.txt check/78_65_78.txt
if errorlevel 1 goto testFailed

%program% 64.3 65 64.3 > 64-3_65_64-3.txt
if errorlevel 1 goto testFailed
fc /b 64-3_65_64-3.txt check/64-3_65_64-3.txt
if errorlevel 1 goto testFailed

%program% 2 -5 1 
if not errorlevel 1 goto testFailed

%program% ad 5 1 
if not errorlevel 1 goto testFailed

%program% 0 2 1  > 0_2_1.txt
if errorlevel 1 goto testFailed
fc /b 0_2_1.txt check/0_2_1.txt
if errorlevel 1 goto testFailed


echo OK
exit /b

:testFailed
echo Testing failed
exit /b

