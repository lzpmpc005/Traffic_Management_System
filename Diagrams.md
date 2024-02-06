# Copy and Paste into PlantUML server: https://www.plantuml.com/plantuml/uml/SyfFKj2rKt3CoKnELR1Io4ZDoSa70000
or import into draw.io

## Class Diagram
@startuml

class Owner {
  + Owner_name: CharField(max_length=20)
  + Owner_age: IntegerField()
  + Owner_phone: CharField(max_length=15)
  + Owner_email: CharField(max_length=30, default='<EMAIL>')
  + Owner_address: CharField(max_length=100)
  + Owner_driver_license: CharField(max_length=10, default='0000000000', blank=False, unique=True)
}

class Plates {
  + Number: CharField(max_length=10, unique=True)
  + Status: CharField(max_length=10, default='available')
}

class Vehicle {
  + Owner: ForeignKey(Owner, null=True, on_delete=models.SET_NULL)
  + Color: CharField(max_length=20)
  + VType: CharField(max_length=50)
  + Speed: IntegerField(default=0)
  + Condition: IntegerField(default=100)
  + PlateNumber: ForeignKey(Plates, null=True, on_delete=models.SET_NULL)
}

class Junction {
  + Address: CharField(max_length=100)
  + Light: IntegerField(default=1)
}

class Log {
  + Junction: CharField(max_length=100)
  + Vehicle_PlateNumber: CharField(max_length=10)
  + Vehicle_Speed: IntegerField()
  + Date: DateField(auto_now_add=True)
  + Time: TimeField(auto_now_add=True)
}

class Fine {
  + fine: IntegerField()
  + owner: ForeignKey(Owner, on_delete=models.SET_NULL, null=True)
  + status: CharField(max_length=10)
  + date: DateField(auto_now_add=True)
}

class DriverLicense {
  + Owner: ForeignKey(Owner, on_delete=models.SET_NULL, null=True)
  + License_Number: CharField(max_length=10)
  + Issue_Date: DateField(auto_now_add=True)
  + Expire_Date: CharField(default="LifeLong")
  + Status: CharField(max_length=10, default='Valid')
  + Score: IntegerField(default=12)
}

Owner --{ Vehicle
Plates --{ Vehicle
Owner --{ Fine
Owner --{ DriverLicense
Owner --{ Log

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