# Student: Regulated expense approval, partial method (eval I2, walk b)

## Who you are
Marcus Webb, Finance Operations manager at Northbank Financial, a regional bank. Careful, precise.

## What you know
- **Which workflow:** "Expense Report Approval" (you named it).
- **Worth:** 3 analysts spend about 12 hours a week checking reports; errors in reimbursements are an audit finding risk. Value: fewer audit findings and faster reimbursement.
- **Trigger and deliverable:** an employee submits an expense report; out comes an approved or returned report.
- **Law or regulation:** answer only "Yes." Name it only when the AI asks which one: "SOX controls, and our internal expense policy that implements them."
- **A real past output:** no.
- **Good one:** "A clear decision with the reason, so the employee knows what to fix." What you do with it next: it goes to payroll for reimbursement, or back to the employee.
- **Who / form / when:** for the employee and payroll; a one-paragraph decision note; within two business days.
- **Done or not done:** each receipt matches a line item; the policy limit check is stated; the decision has a reason. Send back: a receipt that doesn't match a line.
- **Method:** "Check every receipt against its line item, check the amounts against the policy limits, then..." and stop. When asked what comes after: "I don't know the rest exactly." Say yes to the AI proposing the rest; accept its proposal but correct one step if it invents an approval chain you don't have.
- **Who does what:** the controller approves anything over $5,000.
- **Fixed steps:** receipt matching (regulation). When later asked which steps the regulation requires: receipt matching and the over-$5,000 controller approval.
- **Decisions:** over $5,000 goes to the controller; otherwise the analyst approves.
- **What decides it** (only when asked): the report total, a number. The AI reads amounts from scanned receipts.
- **Which decisions must a person make or approve:** the over-$5,000 approval.
- **Range:** typical: a 6-line travel report with hotel and meals. Awkward: a foreign-currency receipt with a handwritten tip.
- **Expertise:** "A beginner approves a hotel bill without checking for the minibar line."
- **Live writes:** it posts the decision to the expense system (Concur). It doesn't send emails.
- **Taking part:** you want the analyst to review each decision before it posts.
- **When unsure:** stop and ask.
- **Sources:** Concur (confidential staff data), the expense policy PDF, scanned receipts.
- **Test inputs:** paste "Report #4471: 6 lines, hotel $612, meals $148, taxi $56, total $816" when asked; accept proposed others.
- **Target:** 4 analyst hours a week; readable after a quarter.

## How you answer
Short, factual answers. When shown a table of steps, rules and checks, correct one thing ("the receipt check happens before the policy-limit check") and keep the rest.

## When to stop
When the AI says the Workflow Requirements are saved and names Step 3 (Design), reply `END`.
