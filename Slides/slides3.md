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

# Traffic Management System 3.0   


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
13/02/2024

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
| <kbd>I</kbd> | Implement Traffic Data Analysis Procedure |
| <kbd>II</kbd> | Generate and Retrieve Traffic Report |
| <kbd>III</kbd> | Detect Congestion |
| <kbd>IV</kbd> | Email Drivers and Suggest Alternative routes |

---

# Class Diagram

<div class="v-main">
 <div style="width: 80%;max-height: 60vh; margin: auto;">

```plantuml {scale: 1}
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


```
 </div>
</div>

---

# Part I Traffic Analysis Report

## Usecase Diagram

<div class="grid grid-cols-1 gap-5 pt-4 -mb-6">

```plantuml {scale: 1}
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

```

</div>


---

# Traffic Analysis Report
## Sequence Diagram

<div class="v-main">
 <div style="width: 70%;max-height: 60vh; margin: auto;">


```plantuml {scale: 1}
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
```

 </div>
</div>

---
layout: default
---

# Part II Detect Congestion and Notify Drivers

## Usecase Diagram

<div class="grid grid-cols-1 gap-5 pt-4 -mb-6">

```plantuml {scale: 1}
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

```
:::figcaption
Congestion Condition:   
In 10 minutes period, Quantity of vehicles passed a specific Junction reachs 30 !
:::
</div>

---

# Detect Congestion and Notify Drivers
## Sequence Diagram

<div class="v-main">
 <div style="width: 55%;max-height: 60vh; margin: auto;">
```plantuml {scale: 1.0}
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

```

 </div>
</div> 
---
layout: center
class: text-center
---

# Thank you for watching

[GitHub](https://github.com/lzpmpc005/Traffic_Management_System/tree/main)
