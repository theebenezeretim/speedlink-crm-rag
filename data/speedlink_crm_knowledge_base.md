# SPEEDLINK CRM KNOWLEDGE BASE

## Metadata

- **Organization:** Speedlink Hi-Tech Solutions Limited / Speedlink Innovation Company
- **Knowledge base purpose:** RAG-optimized knowledge base for CRM conversational AI (chatbot) covering commercial services and research & innovation support
- **Major domains:**
  1. Domain 1: Commercial Services CRM (Speedlink Hi-Tech Solutions Limited)
  2. Domain 2: Research & Innovation CRM (Speedlink Innovation Company)
- **Source document title:** SPEEDLINK HI-TECH SOLUTIONS LIMITED — UNIFIED CHATBOT CONVERSATION BRAIN (ALL SERVICES); SPEEDLINK INNOVATION COMPANY — RESEARCH & INNOVATION CHATBOT MODULE (CRM SYSTEM)

---

# DOMAIN 1: COMMERCIAL SERVICES CRM

## COMMERCIAL — GENERAL — UNIVERSAL OPENING
**Type:** RESPONSE_TEMPLATE
**Trigger:** Client: Hello / Hi / Good morning
**Content:**
> Good Day, welcome to Speedlink Hi-tech Solutions Limited.
> How can we assist you today?

## COMMERCIAL — GENERAL — SERVICE IDENTIFICATION
**Type:** WORKFLOW
**Trigger:** Client: I need internet / training / exam / office space
**Action:** Present the list of available services and ask the client to choose one.
**Content:**
> Thank you 👍
> Which of our services are you interested in?
> - Co-working Space / Office Space
> - FTTH Internet / Broadband
> - Training Programs
> - Pearson VUE Exam Registration

## COMMERCIAL — WORKSPACE — ENTRY
**Type:** WORKFLOW
**Trigger:** Client: I need workspace
**Action:** Ask what they intend to use the workspace for or what kind of job they do.
**Content:**
> Great 👍
> What do you want to use the workspace for?
> OR
> What kind of job do you do?

## COMMERCIAL — WORKSPACE — RECOMMENDATION LOGIC
**Type:** DECISION_LOGIC
**Content:**
IF: Customer is a freelancer, remote worker, or student
THEN: Recommend Shared Coworking Space or Personal Workspace

IF: Customer needs business, meetings, or corporate use
THEN: Recommend Executive Office or Boardroom

IF: Customer needs training, tech, or group work
THEN: Recommend Training Hall or ICT Simulation Room

## COMMERCIAL — WORKSPACE (SHARED COWORKING SPACE) — PRICING
**Type:** PRICING
**Content:**
- Hourly: ₦1,500
- Daily: ₦5,000
- Monthly: ₦50,000

## COMMERCIAL — WORKSPACE (SHARED COWORKING SPACE) — AMENITIES
**Type:** FACT
**Content:**
- Fast & reliable internet
- 24/7 power supply
- Smart surveillance system
- Access control
- Water access
- Canteen area
- Paid printing/scanning service

## COMMERCIAL — WORKSPACE (PERSONAL WORKSPACE) — PRICING
**Type:** PRICING
**Content:**
- Hourly: ₦3,000
- Daily: ₦8,000
- Weekly: ₦22,000
- Monthly: ₦85,000

## COMMERCIAL — WORKSPACE (PERSONAL WORKSPACE) — AMENITIES
**Type:** FACT
**Content:**
- Fast internet
- 24/7 power supply
- Smart surveillance system
- Access control
- Water access
- Canteen area
- Printing/scanning service
- Private office space
- Parking space
- Extra desk option (₦35,000/month)

## COMMERCIAL — WORKSPACE (EXECUTIVE OFFICE) — PRICING
**Type:** PRICING
**Content:**
- Monthly: ₦200,000
- Quarterly: ₦450,000 (discounted from ₦600,000)

## COMMERCIAL — WORKSPACE (EXECUTIVE OFFICE) — AMENITIES
**Type:** FACT
**Content:**
- Fast internet
- 24/7 power supply
- Smart surveillance system
- Access control
- Water, tea/coffee
- Canteen access
- Printing/scanning service
- Private office space
- Virtual secretarial service
- Parking space
- 2-hour weekly boardroom access
- Lounge access
- Smart screen
- Visitor management

## COMMERCIAL — WORKSPACE (CEO EXECUTIVE OFFICE) — PRICING
**Type:** PRICING
**Content:**
- Daily: ₦200,000
- Weekly: ₦700,000

## COMMERCIAL — WORKSPACE (CEO EXECUTIVE OFFICE) — AMENITIES
**Type:** FACT
**Content:**
- Fast internet
- 24/7 power supply
- Smart surveillance system
- Access control
- Water, tea/coffee
- Private office + washroom
- Executive workstation + visitor seats
- 6-seater virtual boardroom
- Video conferencing facility
- Sofa lounge setup
- Dual smart screens
- Parking space
- Lounge access
- Secretarial service

## COMMERCIAL — WORKSPACE (BOARDROOM) — PRICING
**Type:** PRICING
**Content:**
- Daily: ₦200,000
- Weekly: ₦800,000

## COMMERCIAL — WORKSPACE (BOARDROOM) — AMENITIES
**Type:** FACT
**Content:**
- Video conferencing facility
- 24/7 power supply
- Smart surveillance system
- Access control
- Tea/coffee
- Writing materials
- 12–15 seating capacity
- Parking space
- Lounge access

## COMMERCIAL — WORKSPACE (TRAINING HALLS) — PRICING
**Type:** PRICING
**Content:**
- Daily: ₦200,000
- Weekly: ₦800,000

## COMMERCIAL — WORKSPACE (TRAINING HALLS) — AMENITIES
**Type:** FACT
**Content:**
- Video conferencing facility
- 24/7 power supply
- Smart surveillance system
- 30–40 seating capacity
- Writing materials
- Canteen access
- Parking space

## COMMERCIAL — WORKSPACE (COMPUTER TRAINING HALL) — PRICING
**Type:** PRICING
**Content:**
- Daily: ₦400,000
- Weekly: ₦1,500,000

## COMMERCIAL — WORKSPACE (COMPUTER TRAINING HALL) — AMENITIES
**Type:** FACT
**Content:**
- 9–11 high-end systems
- Internet access
- 24/7 power supply
- Video conferencing
- 9–12 seating capacity
- Printing/scanning service
- Canteen access

## COMMERCIAL — WORKSPACE (MINI TRAINING HALL) — PRICING
**Type:** PRICING
**Content:**
- Daily: ₦150,000
- Weekly: ₦600,000

## COMMERCIAL — WORKSPACE (MINI TRAINING HALL) — AMENITIES
**Type:** FACT
**Content:**
- Internet
- 24/7 power supply
- Video conferencing
- Printing/scanning
- Writing materials
- Parking space

## COMMERCIAL — WORKSPACE (ICT SIMULATION ROOM) — PRICING
**Type:** PRICING
**Content:**
- Daily: ₦200,000
- Weekly: ₦900,000

## COMMERCIAL — WORKSPACE (ICT SIMULATION ROOM) — AMENITIES
**Type:** FACT
**Content:**
- Internet
- 24/7 power supply
- Video conferencing
- 6 seating capacity
- Printing/scanning
- Canteen access

## COMMERCIAL — WORKSPACE — PRICING REQUEST HANDLING
**Type:** WORKFLOW
**Trigger:** Client: How much is it?
**Action:** Ask which workspace type the client is interested in before revealing full pricing and amenities.
**Content:**
> Great 👍
> Which workspace are you interested in?
> - Shared Coworking Space
> - Personal Workspace
> - Executive Office
> - Boardroom / Training Hall
>
> Once you confirm, I'll give you full pricing and amenities.

## COMMERCIAL — WORKSPACE — CLOSING
**Type:** WORKFLOW
**Trigger:** Client: I want it
**Action:** Collect full name, workspace type, and start date; offer to generate invoice.
**Content:**
> Perfect 👍
> Please provide:
> - Full name
> - Workspace type
> - Start date
>
> Shall I generate your invoice now?

## COMMERCIAL — WORKSPACE — CORE RULES
**Type:** BUSINESS_RULE
**Content:**
- Always recommend first before pricing dump
- Always store pricing internally for instant response
- Only reveal full details when asked

## COMMERCIAL — FTTH INTERNET — INQUIRY
**Type:** WORKFLOW
**Trigger:** Client: I need internet
**Action:** Thank the client and request their location to check coverage.
**Content:**
> Thank you for your interest in our FTTH service 👍
> May I have your location to check coverage?

## COMMERCIAL — FTTH INTERNET — COVERAGE EXPLANATION
**Type:** FACT
**Content:**
> We provide high-speed fiber internet for streaming, work, CCTV, gaming, and smart homes.

## COMMERCIAL — FTTH INTERNET — PRICING
**Type:** PRICING
**Trigger:** Client: How much?
**Content:**
> Plans include:
> - Smart Starter: ₦20,000
> - Smart Premium: ₦28,650
> - Smart Diamond: ₦36,750
> - Smart Gold: ₦52,500
>
> Installation depends on your location.

## COMMERCIAL — FTTH INTERNET — COVERAGE RESULT
**Type:** CONDITION
**Content:**
IF Covered:
> Good news 👍 Your area is covered.
> Setup fee is ₦[amount]. Shall we proceed?

IF Not Covered:
> Your location is outside FTTH coverage.
> We can offer Radio Broadband instead. Should I check pricing?

## COMMERCIAL — FTTH INTERNET — CLOSING
**Type:** WORKFLOW
**Trigger:** Client: I want it
**Content:**
> Perfect 👍 Let's proceed.
> Shall I send your invoice now?

## COMMERCIAL — TRAINING — INQUIRY
**Type:** WORKFLOW
**Trigger:** Client: I want training
**Content:**
> Great 👍 Which course are you interested in?

## COMMERCIAL — TRAINING — COURSE LIST
**Type:** RESPONSE_TEMPLATE
**Content:**
> We offer:
> - Data Analytics
> - Web Development
> - UI/UX
> - Cybersecurity
> - Cloud Computing
> - Digital Marketing
> - Graphics Design
> - Mobile App Development
> - Solar Systems
> - SIWES Training
>
> Which one are you choosing?

## COMMERCIAL — TRAINING — QUALIFICATION
**Type:** QUALIFICATION_REQUIREMENT
**Trigger:** Client: I want [course]
**Content:**
> Perfect 👍
> Are you:
> - Beginner or experienced?
> - Job, business, or personal growth?
> - When do you want to start?

## COMMERCIAL — TRAINING — PRICING
**Type:** PRICING
**Trigger:** Client: How much?
**Content:**
> Cost depends on course and mode (online/onsite).
> Would you like me to share full breakdown for your selected course?

## COMMERCIAL — TRAINING — CLOSING
**Type:** WORKFLOW
**Content:**
> Shall we secure your training slot today?

## COMMERCIAL — TRAINING — PAYMENT CONFIRMATION
**Type:** PAYMENT_INFORMATION
**Content:**
> Payment confirmed 👍
> You will receive LMS access and onboarding details shortly.

## COMMERCIAL — PEARSON VUE — INQUIRY
**Type:** WORKFLOW
**Trigger:** Client: I want exam registration
**Content:**
> Great 👍
> Which exam are you registering for?

## COMMERCIAL — PEARSON VUE — REGISTRATION
**Type:** QUALIFICATION_REQUIREMENT
**Action:** Collect full name, exam type, and location. Registration takes 24–48 hours.
**Content:**
> To proceed, I need:
> - Full name
> - Exam type
> - Location
>
> Registration takes 24–48 hours.

## COMMERCIAL — PEARSON VUE — PRICING LOGIC
**Type:** PRICING
**Content:**
> Exam fee includes:
> - Base fee (USD)
> - 6% bank charge
> - 7.5% VAT
> - Exchange rate conversion
>
> Payment must be same day due to rate changes.

## COMMERCIAL — PEARSON VUE — PAYMENT CLOSE
**Type:** PAYMENT_INFORMATION
**Content:**
> Your total is ₦[amount].
> Shall I send invoice now?

## COMMERCIAL — PEARSON VUE — COMPLETION
**Type:** OUTCOME
**Content:**
> Exam scheduled 👍
> You will receive full details via email.

## COMMERCIAL — OBJECTION HANDLING — PRICE OBJECTION
**Type:** RESPONSE_TEMPLATE
**Trigger:** Client: Too expensive
**Content:**
> Is it price or value concern?
> If it solves your problem, would it still feel expensive?

## COMMERCIAL — OBJECTION HANDLING — DELAY
**Type:** RESPONSE_TEMPLATE
**Trigger:** Client: I need time
**Content:**
> What exactly do you need time to think about?

## COMMERCIAL — OBJECTION HANDLING — NO MONEY
**Type:** RESPONSE_TEMPLATE
**Trigger:** Client: I don't have money
**Content:**
> If budget wasn't an issue, would you start today?

## COMMERCIAL — OBJECTION HANDLING — NOT NOW
**Type:** RESPONSE_TEMPLATE
**Trigger:** Client: Not now
**Content:**
> What would need to change for this to become a priority?

## COMMERCIAL — FOLLOW-UP SYSTEM — SCHEDULE
**Type:** FOLLOW_UP
**Content:**
- 24 Hours: "Just checking in, are you ready to proceed?"
- 48 Hours: "We can still secure your slot today."
- Final: "Should I keep your request open or close it?"

---

# GLOBAL CRM BEHAVIORAL RULES

## COMMERCIAL — GLOBAL — CORE CHATBOT RULES
**Type:** BUSINESS_RULE
**Content:**
- Always respond with questions
- Always guide toward decision
- Never leave conversation open-ended
- Always push toward next step
- Always confirm service type first
- Always collect location or intent early
- Always end with CTA (invoice / registration / proceed)

## COMMERCIAL — GLOBAL — FINAL OBJECTIVE
**Type:** FACT
**Content:**
This chatbot system is designed to:
- Identify customer intent quickly
- Qualify leads automatically
- Guide conversation toward payment
- Reduce human intervention
- Increase conversion rate across all services

---

# DOMAIN 2: RESEARCH & INNOVATION CRM

## RESEARCH — GENERAL — SERVICE CONTEXT
**Type:** FACT
**Content:**
Speedlink Innovation Company provides structured academic and technical research support for:
- Undergraduate final year projects
- HND / BSc / BEng capstone projects
- MSc research projects
- MPhil & PhD thesis support
- Journal publication preparation

## RESEARCH — GENERAL — UNIVERSAL OPENING
**Type:** WORKFLOW
**Trigger:** Client: Hello / Hi / I need project help
**Action:** Thank the client and request level of study, course of study, project topic (if available), institution, deadline, and type of support needed.
**Content:**
> Thank you for contacting Speedlink Innovation Company.
> We provide structured research and technical support for science, engineering, and technology-based projects.
>
> To assist you better, kindly share:
> - Level of study
> - Course of study
> - Project topic (if available)
> - Institution
> - Deadline
> - Type of support needed

## RESEARCH — GENERAL — NO TOPIC FLOW
**Type:** WORKFLOW
**Trigger:** Client: I don't have a topic
**Action:** Offer to help develop a research topic based on industry relevance, research gaps, feasibility, and available tools. Collect specialization area, preferred field, and supervisor requirements. Provide 3–5 suggested topics.
**Content:**
> No problem 👍
> We can help you develop a research topic based on:
> - Industry relevance
> - Research gaps
> - Feasibility
> - Available tools
>
> Kindly share:
> - Your specialization area
> - Preferred field (AI, IoT, Solar, Robotics, Power Systems, etc.)
> - Supervisor requirements (if any)
>
> We will suggest 3–5 strong research topics for you.

## RESEARCH — GENERAL — SERVICE EXPLANATION
**Type:** FACT
**Trigger:** Client: What do you do?
**Content:**
> We provide structured research and technical development support:
>
> Academic Support
> - Proposal structuring
> - Literature review guidance
> - Methodology development
> - Data analysis
>
> Technical Support
> - Python simulations
> - AI model development
> - Embedded systems design
> - Robotics systems
> - Power systems simulations
>
> We ensure academic integrity while guiding your development.

## RESEARCH — GENERAL — CLIENT WITH TOPIC
**Type:** WORKFLOW
**Trigger:** Client: My topic is [X]
**Action:** Confirm whether simulation or hardware-based, whether a working prototype is needed, supervisor requirements, and allowed tools. Then outline system design, components, methodology, and implementation plan.
**Content:**
> Excellent topic 👍
> To proceed, please confirm:
> - Simulation or hardware-based?
> - Do you need a working prototype?
> - Supervisor requirements?
> - Allowed tools (MATLAB, Arduino, Proteus, etc.)
>
> We will then outline:
> - System design
> - Components
> - Methodology
> - Implementation plan

## RESEARCH — GENERAL — PRICE FLOW
**Type:** PRICING
**Trigger:** Client: How much?
**Content:**
> Pricing depends on:
> - Level of study
> - Complexity
> - Technical requirements
> - Timeline
>
> We offer:
> - Basic Advisory Support
> - Standard Development Support
> - Advanced Technical & Prototype Support
>
> Kindly share your project details for a proper quotation.

## RESEARCH — GENERAL — CLIENT EXPECTATION CLARITY
**Type:** BUSINESS_RULE
**Trigger:** Client: Will you do everything for me?
**Content:**
> We operate under academic integrity guidelines.
> We provide:
> - Structured guidance
> - Technical design support
> - Simulation assistance
> - Documentation structuring
>
> You remain actively involved to ensure understanding and defense ability.

## RESEARCH — GENERAL — DEADLINE FLOW
**Type:** WORKFLOW
**Trigger:** Client: Can you finish in 2 weeks?
**Action:** Explain that timeline depends on project scope. Ask client to confirm scope. Provide milestone-based timeline.
**Content:**
> Timeline depends on project scope.
> Please confirm:
> - Proposal only
> - Full simulation
> - Hardware prototype
> - Full thesis documentation
>
> We will provide a milestone-based timeline.

## RESEARCH — GENERAL — CONFIDENTIALITY
**Type:** FACT
**Trigger:** Client: Is my project confidential?
**Content:**
> Yes 👍
> We maintain strict confidentiality:
> - NDA available on request
> - Secure handling of documents
> - Restricted internal access
>
> Your intellectual property is protected.

## RESEARCH — GENERAL — POSTGRADUATE FLOW
**Type:** QUALIFICATION_REQUIREMENT
**Trigger:** Client: I'm MSc/PhD student
**Content:**
> For postgraduate research, we support:
> - Advanced methodology design
> - Experimental structuring
> - Statistical analysis
> - Journal formatting (IEEE, Elsevier, Springer)
> - Reviewer response support
>
> Kindly share:
> - Abstract
> - Supervisor feedback
> - Target journal
> - Data status
>
> We will structure next steps.

## RESEARCH — GENERAL — PAYMENT FLOW
**Type:** PAYMENT_INFORMATION
**Trigger:** Client: How do I pay?
**Content:**
> Our process:
> 1. Consultation
> 2. Scope confirmation
> 3. Quotation
> 4. Agreement
> 5. 60% upfront payment
> 6. Milestone delivery
> 7. Final balance
>
> We accept bank and online transfers.

## RESEARCH — FOLLOW-UP SYSTEM — SILENT CLIENT
**Type:** FOLLOW_UP
**Trigger:** If client is silent
**Content:**
> Hello 👋
> We are following up on your research request.
> Please let us know:
> - If you wish to proceed
> - If you need clarification
> - If your timeline has changed
>
> We are available to assist.

## RESEARCH — GENERAL — CONVERSION MESSAGE
**Type:** RESPONSE_TEMPLATE
**Content:**
> Based on your project scope, we recommend a structured support package.
> If approved, we can begin onboarding immediately to meet your deadline.
> Kindly confirm to proceed with the service agreement.

---

# RESEARCH CRM RULES

## RESEARCH — GLOBAL — CORE RULES
**Type:** BUSINESS_RULE
**Content:**
- Always ask for project details first
- Never give pricing without scope clarity
- Always maintain academic integrity tone
- Always guide, not replace student work
- Always move conversation toward scope + agreement

## RESEARCH — GLOBAL — OBJECTIVE
**Type:** FACT
**Content:**
Convert research inquiries into structured, ethical, scoped academic support engagements while maintaining professionalism and clarity.
