-- Drone Pin.app: pick a folder of drone stills; the client and address come from the
-- SSD's "Client | Address" folder name (asks only when that isn't enough); review + export in the browser.
set tool to "/Users/10xhunter/Documents/Hunters Second Brain/projects/drone-pin/app.sh"
set f to choose folder with prompt "Pick the folder of drone stills (e.g. …/Done/Drone)"
set p to POSIX path of f
set r to do shell script quoted form of tool & " " & quoted form of p
if r is "NEED_ADDRESS" then
	-- Guess from a folder named like "Kollosche | 5 Esther Place, Surfers Paradise".
	set guess to do shell script "print -r -- " & quoted form of p & " | tr '/' '\\n' | grep '|' | tail -1 | sed 's/.*| *//'"
	set a to text returned of (display dialog "Property address (finds the lot boundary):" default answer guess with title "Drone Pin")
	display notification "Reading GPS and finding the lot…" with title "Drone Pin"
	set r to do shell script quoted form of tool & " " & quoted form of p & " " & quoted form of a
end if
if r starts with "ERROR=" then
	display dialog (text 7 thru -1 of r) with title "Drone Pin couldn't start" buttons {"OK"} default button 1 with icon stop
end if
