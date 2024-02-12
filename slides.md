---
theme: seriph
background: https://images.unsplash.com/photo-1465447142348-e9952c393450?q=80&w=3992&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D
class: text-center
highlighter: shikiji
lineNumbers: false
info: |
  ## Slidev Starter Template
  Presentation slides for developers.

  Learn more at [Sli.dev](https://sli.dev)
drawings:
  persist: false
transition: slide-left
title: traffic management system
mdc: true
---

# Traffic Management System 2.0   


<div class="absolute top-1/1.9 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
  <button title="Open in python" class="text-xl slidev-icon-btn  !border-none !hover:text-white">
    <img src="https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg" alt="Python Logo" style="height: 30px; width: 30px;">
  </button>
  <button title="Open in django" class="text-xl slidev-icon-btn  !border-none !hover:text-white">
    <img src="https://upload.wikimedia.org/wikipedia/commons/7/75/Django_logo.svg" alt="Django Logo" style="height: 30px; width: 70px;">
  </button>
  <button title="Open in PostgreSQL" class="text-xl slidev-icon-btn  !border-none !hover:text-white">
    <img src="https://upload.wikimedia.org/wikipedia/commons/2/29/Postgresql_elephant.svg" alt="PostgreSQL Logo" style="height: 30px; width: 30px;">
  </button>
</div>

<div class="pt-12">
  <span @click="$slidev.nav.next" class="px-2 py-1 rounded cursor-pointer" hover="bg-white bg-opacity-10">
    HONGTAO AND VINCENT <carbon:arrow-right class="inline"/>
  </span>
</div>
06/02/2024

<div class="abs-br m-6 flex gap-2">
  <button @click="$slidev.nav.openInEditor()" title="Open in Editor" class="text-xl slidev-icon-btn opacity-50 !border-none !hover:text-white">
    <carbon:edit />
  </button>
  <a href="https://github.com/lzpmpc005/Traffic_Management_System" target="_blank" alt="GitHub" title="Open in GitHub"
    class="text-xl slidev-icon-btn opacity-50 !border-none !hover:text-white">
    <carbon-logo-github />
  </a>
</div>

<!--
The last comment block of each slide will be treated as slide notes. It will be visible and editable in Presenter Mode along with the slide. [Read more in the docs](https://sli.dev/guide/syntax.html#notes)
-->

---

# Tasks

|     |     |
| --- | --- |
| <kbd>I</kbd> | Rewrite Register Vehicle and Logging |
| <kbd>II</kbd> | Violation Detection Procedure |
| <kbd>III</kbd> | Issue Fine and Related Procedure |
| <kbd>IV</kbd> | Python Scripts to Simulate Each Process |

---

# Class Diagram

<div class="grid grid-cols-1 gap-5 pt-4 -mb-6">

```plantuml {scale: 1}
@startuml

class Owner {
  + Owner_name
  + Owner_age
  + Owner_phone
  + Owner_email
  + Owner_address
  + Owner_driver_license
}

class Plates {
  + Number
  + Status
}

class Vehicle {
  + Owner
  + Color
  + VType
  + Speed
  + Condition
  + PlateNumber
}

class Junction {
  + Address
  + Light
}

class Log {
  + Junction
  + Vehicle_PlateNumber
  + Vehicle_Speed
  + Date
  + Time
}

class Fine {
  + fine
  + owner
  + status
  + date
}

class DriverLicense {
  + Owner
  + License_Number
  + Issue_Date
  + Expire_Date
  + Status
  + Score
}

Owner "1" -- "N" Vehicle
Plates "1" -- "1" Vehicle
Owner "1" -- "N" Fine
Owner "1" -- "1" DriverLicense
Owner "1" -- "N" Log

@enduml

@enduml

```

</div>

---

# Part I predict congestion times and suggest alternative routes

## Usecase Diagram

<div class="grid grid-cols-1 gap-5 pt-4 -mb-6">

```plantuml {scale: 1}
@startuml
left to right direction
actor Driver
rectangle "Traffic Congestion System" {
    Driver -- (Receive Congestion Notification)
    (Receive Congestion Notification) --> (Send Congestion Notification Email)
}
@enduml


```

</div>

---

# predict congestion times and suggest alternative routes: Sequence Diagram

<div class="grid grid-cols-2 gap-3 pt-4 -mb-3">


```plantuml {scale: 1}
@startuml
participant Driver
participant "Traffic Congestion System" as System
Driver -> System: Receive Congestion Notification
activate System
System -> System: Send Congestion Notification Email
activate System
System --> Driver: Confirmation
deactivate System
@enduml

```
:::figcaption
Violations     
1. Illegal Driving    
2. Running Red Light   
3. Fake Plate Number   
4. Illegal Parking   
5. Different Levels of Speeding 
:::


</div>

---
layout: default
---

# Part II Issue Fine

## Usecase Diagram

<div class="grid grid-cols-1 gap-5 pt-4 -mb-6">

```plantuml {scale: 1}
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

```

</div>

---

# Issue Fine: Sequence Diagram


<div class="v-main">
  <div style="width: 70%; max-height: 60vh; margin: auto;">
```plantuml 
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

```

  </div>
</div>


---
layout: default
---

