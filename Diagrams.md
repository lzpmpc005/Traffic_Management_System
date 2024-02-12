# Copy and Paste into PlantUML server: https://www.plantuml.com/plantuml/uml/SyfFKj2rKt3CoKnELR1Io4ZDoSa70000
or import into draw.io

## Class Diagram
@startuml

Left to Right Direction

class Owner {
  + Owner_id
  + Owner_name
  + Owner_age
  + Owner_phone
  + Owner_email
  + Owner_address
  + Owner_driver_license
}

class Plates {
  + Plates_id
  + PlateNumber
  + Status
}

class Vehicle {
  + Vehicle_id
  + Owner_id
  + Color
  + VType
  + Speed
  + Condition
  + PlateNumber
}

class Junction {
  + Junction_id
  + Junction_Address
  + Junction_Type
  + Light
}

class Log {
  + Junction_id
  + PlateNumber
  + Vehicle_Speed
  + Date
  + Time
}

class Fine {
  + fine_id
  + fine
  + owner_id
  + status
  + date
}

class DriverLicense {
  + Owner_id
  + License_Number
  + Issue_Date
  + Expire_Date
  + Status
  + Score
}

class AnalysisReport {
  + Junction_id
  + Vehicle_Quantity
  + Date
  + Time
}

Log - Junction
Log -- AnalysisReport
Owner "1" -- "N" Vehicle
Plates "1" -- "1" Vehicle
Owner "1" -- "N" Fine
Owner "1" -- "1" DriverLicense
Vehicle -- Log

@enduml

## Register_Vehicle: Usecase Diagram

@startuml
Left to Right Direction
skinparam packageStyle rectangle

actor Owner as User
actor DMV as DMV
rectangle "Register Vehicle" {
  usecase "Provide Vehicle details" as UC1
  usecase "Check Owner Qualification" as UC2
  usecase "Validate Vehicle" as UC3
  usecase "Assign Plate Number" as UC4
}

User --> UC1
UC1 --> UC2 
UC2 --> UC3
UC3 --> UC4
DMV --> UC2
DMV --> UC3
DMV --> UC4

@enduml


## Logging and violation detecting: Usecase Diagram

@startuml

actor SkyEye as User
actor Police as P
actor DMV

usecase "Logging" as UC1
usecase "Detect Violation" as UC2
usecase "Report to Police" as UC3

User -> UC1
DMV --> UC1
UC1 -> UC2 : <<include>>
UC2 -> UC3 : <<include>>
UC3 --> P

@enduml

## Logging and violation detecting: Sequence Diagram
@startuml
actor SkyEye as User
actor DMV
actor Police as P

User --> User: Detect Vehicle, Light, Speed
User --> DMV: Retrieve Owner, Vehicle, Driver License
DMV --> User: Return Owner, Vehicle, Driver License
User --> User: Check Violation

User --> P: Report Violation Information

@enduml


## Issue Fine Usecase Diagram
@startuml
Left to Right Direction
actor Police as User
actor Owner as O
actor DMV
actor Outlook as Ou

usecase "Receive Violation Information" as UC1
usecase "Calculate Fine" as UC5
usecase "Update Driver License" as UC6
usecase "Generate Fine Notice" as UC7
usecase "Update Fine" as UC8
usecase "Send Notice To Owner By Email" as UC10
usecase "Pay Fine" as UC11
usecase "Update Fine" as UC12
usecase "Self Update" as UC13

User --> UC1
UC1 -> UC5
UC5 --> UC7
UC6 --> UC5 : <<extend>>
UC7 -> UC10
UC5 -> UC8 : <<include>>
DMV -> UC6
UC10 -> O
O --> UC11
UC11 -> UC12 : <<include>>
User --> UC11
UC13 -> UC11 : <<extend>>
Ou --> UC10
@enduml

## Issue Fine Sequence Diagram
@startuml

actor SkyEye as S
actor Police as User
actor DMV
actor Outlook as Ou
actor Owner as O

S --> User: Send Violation Information
User --> DMV: Retrieve Owner, Vehicle, Driver License
DMV --> User: Return Owner, Vehicle, Driver License
User --> User: Calculate Fine
User --> DMV: Update Driver License
User--> User: Generate Fine Notice
User --> Ou: Send request
Ou --> O: Send Notice Email
O --> User: Pay Fine
User --> User: Update Fine
User --> User: Self Update

@enduml


## Analyse Traffic Flow Usecase Diagram
@startuml

left to right direction

actor "SkyEye" << device >> as S
actor "Police" << human >> as P

rectangle "Traffic Management System" {
 
  usecase (Log Traffic Flow) as UC1
  usecase (Retrieve Traffic Report) as UC3
  usecase (Generate Traffic Report) as UC4
  usecase (Predict Congestion) as UC5

  rectangle "DMV"{
    usecase (Triger Updating\nAnalysis Report Table) as UC2
    usecase (Store Log Information) as UC7
    usecase (Retrieve Analysis Data) as UC8
  }
  

S --> UC1
UC1 --> UC7
UC7 -> UC2: << include >>

P --> UC3
UC3 --> UC4: << include >>
UC4 --> UC8

UC1 --> UC5: << include >>
UC5 --> UC8

@enduml
  
## Analyse Traffic Flow Sequence Diagram

@startuml

== Traffic Analysis ==

actor "SkyEye" as S
actor "Police" as P

participant "Traffic Analysis System" as TAS

participant "Department of Motor Vehicle" as DMV

S -> DMV : Log Traffic information
activate DMV
DMV -> DMV : Auto Updating Traffic Data
P -> TAS : Retrieve Traffic Report
deactivate DMV
activate TAS
TAS -> DMV : Get Traffic Data
DMV -> TAS : Return Traffic Data
TAS -> TAS : Generate Traffic Report
TAS -> TAS : Open Report

@enduml

## Detect Congestion and Notify UseCase Diagram
@startuml

actor SkyEye as S
actor EmailServer as E
rectangle "Traffic Management System" {
   usecase (Log Traffic Information) as UC1
   usecase (Retrieve Traffic Data) as UC2
   usecase (Check Congestion) as UC4
   usecase (Send Notification Email) as UC5
}

S -> UC1
UC1 --> UC2
UC2 -> UC4
UC4 -> UC5: <include>
E -> UC5

@enduml

## Detect Congestion and Notify Sequence Diagram

@startuml

== Traffic Logging ==

actor "SkyEye" as S
participant "Department of Motor Vehicle" as DMV
participant "Email Server" as ES
actor "Driver" as D

S -> DMV : Log Traffic information
activate DMV
DMV -> DMV : Auto Updating Traffic Data
S -> DMV : Get Traffic Data
DMV -> S : Return Traffic Data
deactivate DMV
S -> S : Check Congestion

== Email Notification ==

S -> ES : Send Congestion Information
activate ES
ES -> D : Email Notification
deactivate ES

@enduml
