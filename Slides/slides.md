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

# traffic management system

PYTHON AND DJANGO

<div class="pt-12">
  <span @click="$slidev.nav.next" class="px-2 py-1 rounded cursor-pointer" hover="bg-white bg-opacity-10">
    HONGTAO AND VINCENT <carbon:arrow-right class="inline"/>
  </span>
</div>

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
layout: default
---

# Table of contents



<Toc maxDepth="1"></Toc> 
---

# Requirements

|     |     |
| --- | --- |
| <kbd>I</kbd> |  Register Vehicle |
| <kbd>II</kbd> | Simulate Recognizing License |

---

# Class Diagram

<div class="grid grid-cols-1 gap-5 pt-4 -mb-6">

```plantuml {scale: 1}
@startuml
left to right direction

class Owner {
  - Id : Integer
  - Name: String
  - Phone: String
  - Email: String
  - Address: String
  + register() : void
}

class Vehicle {
  - Number: String
  - Owner_id: Owner_id
  - Color: String
  - Producer: String
  - Type: String
  - Year: Integer
  + register(Owner: owner_id) : void
}

class Junction {
  - Address: String
  + registerJunction() : void
  + recognizeLicense(Vehicle : Color, Producer, Type) : string
}

Owner -- Vehicle
Junction -- Vehicle

@enduml

```
:::figcaption
We defined three classes: Junction, Vehicle, Owner. 
We use phone number to distinguish each owner. 
We use owner_id to connect each vehicle to its owner.
We use "color + producer + type" to recognize vehicles.
:::

</div>


---
layout: image-left
image: https://images.unsplash.com/photo-1517676109075-9a94d44145d1?q=80&w=3648&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D
---

# Part I register vehicle

This part design the models about the vehicle![^1]

<arrow v-click="[3, 4]" x1="400" y1="420" x2="230" y2="330" color="#564" width="3" arrowSize="1" />

[^1]: [Learn More](https://sli.dev/guide/syntax.html#line-highlighting)

<style>
.footnotes-sep {
  @apply mt-20 opacity-10;
}
.footnotes {
  @apply text-sm opacity-75;
}
.footnote-backref {
  display: none;
}
</style>
---
transition: slide-up
level: 2
---

# Rigester_vehicle

### vehicle details

|     |     |
| --- | --- |
| <kbd>nubmer</kbd> |  models.CharField(max_length=10) |
| <kbd>owner_id</kbd> | database allocation id |
| <kbd>color</kbd> | models.CharField(max_length=10) |
| <kbd>producer</kbd> | models.CharField(max_length=10) |
| <kbd>type</kbd> | models.CharField(max_length=10) |
| <kbd>year</kbd> | models.IntegerField |

---

# Register_Vehicle: Usecase Diagram

<div class="grid grid-cols-1 gap-5 pt-4 -mb-6">

```plantuml {scale: 1}
@startuml
left to right direction
skinparam actor {
    BackgroundColor DarkSeaGreen
    BorderColor DarkSlateGray
}

skinparam usecase {
    BackgroundColor LightCyan
    BorderColor DarkSlateGray
}

actor User as "User"
rectangle "Register Vehicle" {
    User --> (User submits vehicle information)
    (User submits vehicle information) --> (Register Vehicle)
}
@enduml

```
:::figcaption

:::
This diagram illustrates the interaction between the "User" and the "Register Vehicle" use case. The user submits vehicle information, which triggers the "Register Vehicle" use case.

</div>


---

# Register_Vehicle: Sequence Diagram

<div class="grid grid-cols-2 gap-5 pt-4 -mb-6">

```plantuml {scale: 1}
@startuml
actor User
participant "User" as User
participant "Django View" as View
participant "Owner" as Owner
participant "Vehicle" as Vehicle
participant "JsonResponse" as Response

User -> View: User submits vehicle information
activate View
alt Validation passed
    View -> Owner: Query Owner by ID
    activate Owner
    View -> Vehicle: Create Vehicle instance
    activate Vehicle
    View -> Response: Return success response
    activate Response
    Response --> User: JSON response with vehicle ID
    deactivate Response
    deactivate Vehicle
    deactivate Owner
else Validation failed
    View -> Response: Return error response
    activate Response
    Response --> User: JSON response with error message
    deactivate Response
end
deactivate View
@enduml
```
:::figcaption
Sequence Diagram:
This diagram illustrates the sequence of interactions between the "User", "Django View", "Owner", "Vehicle", and "JsonResponse" during the vehicle registration process. The user submits vehicle information, which is processed by the Django view. If validation passes, the view queries the owner, creates a vehicle instance, and returns a success response. If validation fails, it returns an error response.
:::

</div>

---

# Part II Recognize Vehicle Plate Number

## Recognize_Vehicle: Usecase Diagram

<div class="grid grid-cols-1 gap-5 pt-4 -mb-6">

```plantuml {scale: 1}
@startuml
left to right direction
skinparam packageStyle rectangle

actor User as User
rectangle "Recognize License" {
  usecase "Provide Vehicle identifiers: Color, Producer, Type" as UC1
  usecase "View Plate Number" as UC2
}

User --> UC1
UC1 --> UC2
@enduml

```

</div>

---

# Recognize_Vehicle: Sequence Diagram

<div class="grid grid-cols-1 gap-5 pt-4 -mb-6">

```plantuml {scale: 1}
@startuml

actor User
participant Controller
participant Vehicle
database Database

User -> Controller: GET Request
activate Controller

Controller -> Controller: Validate Request Parameters
alt Valid Parameters
  Controller -> Database: Query Database
  activate Database
  Database --> Vehicle: Query
  deactivate Database
  alt Vehicle Found
    Controller --> User: JsonResponse{'Plate_number': vehicle.Number}
  else Vehicle Not Found
    Controller --> User: JsonResponse{'error': "Vehicle not found"}, status=404
  end
else Invalid Parameters
  Controller --> User: JsonResponse{'error': "Validation error"}, status=400
end

deactivate Controller
@enduml

```

</div>

