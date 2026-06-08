# Evaluation Progress Log

## Overview
This document tracks how the RAG system improves over time.

Each run includes:
- **Corpus Status:** How many chunks, from which sources
- **Changes Since Last Run:** What was modified to improve results
- **Evaluation Results:** Responses to all 6 test questions with expected vs. actual

**Key Note:** Early runs may have poor performance due to incomplete corpus (some sources couldn't be scraped with basic HTTP requests). As sources are added via improved scraping (e.g., Playwright for JavaScript-heavy sites), accuracy improves.


## Run #1 — 2026-06-07 22:24:34

### Corpus Status
- **Total chunks:** 40
- **Sources ingested:** 6
- **Sources breakdown:**
  - `7` chunks from https://anderscpa.com/learn/blog/understanding-employee-bene...
  - `4` chunks from https://turbotax.intuit.com/tax-tips/jobs-and-career/guide-t...
  - `6` chunks from https://www.cigna.com/knowledge-center/hdhp-vs-ppo-plans...
  - `14` chunks from https://www.dol.gov/agencies/ebsa/about-ebsa/our-activities/...
  - `2` chunks from https://www.dol.gov/general/topic/health-plans/erisa...
  - `7` chunks from https://www.randstadusa.com/job-seeker/career-advice/salary/...

### Changes Since Last Run
Initial ingestion: requests + BeautifulSoup for 10 sources; 4 sources (MetLife, FHB, Woven Capital, Reddit) blocked/insufficient even with Playwright fallback. 6 sources successfully ingested.

### Evaluation Results

#### Q1: Why should someone choose to max out their medical FSA account?

**Expected:**
> You should max out your medical FSA only if you have predictable medical expenses (prescriptions, glasses, copays) that you'll incur within the plan year, because contributions are pre-tax. However, medical FSAs have a strict 'use it or lose it' rule—unused money is forfeited (though some employers allow a small grace period or up to $610 carryover in 2026)—so you shouldn't max out if you're uncertain about expenses.

**System Response:**
> According to the context, maxing out a medical FSA account can provide tax benefits as the money contributed comes out of your paycheck before you pay tax on it. Additionally, the funds in an FSA can be used for medical expenses not covered by insurance, such as dental or vision expenses. However, it's essential to note that any money in your FSA that you don't spend by the end of the year will be lost due to the 'use it or lose it' provision.

Sources:
[1] https://turbotax.intuit.com/tax-tips/jobs-and-career/guide-to-your-employers-benefits-programs-tax-wise-401k-matching-hsas-flexible-etc/L74Iljjyz
[2] https://anderscpa.com/learn/blog/understanding-employee-benefits-guide-for-recent-graduates/

**Sources Cited:**
• https://anderscpa.com/learn/blog/understanding-employee-benefits-guide-for-recent-graduates/
• https://turbotax.intuit.com/tax-tips/jobs-and-career/guide-to-your-employers-benefits-programs-tax-wise-401k-matching-hsas-flexible-etc/L74Iljjyz

#### Q2: If my stocks at a company mature only after 5 years, do I need to remain with the company to get my money's worth?

**Expected:**
> Yes, you must remain with the company until the shares vest (mature). If you leave before 5 years, unvested shares are forfeited and you lose that equity compensation. However, once shares vest and are delivered to you, you own them and they can't be clawed back if you leave.

**System Response:**
> According to the context, when considering stock options, you should "curate a list of specific questions. Ask about the vesting schedule to know how long your money is tied up." This implies that the vesting schedule is important to understand, as it determines how long your money is tied up. If your stocks mature only after 5 years, it is likely that you will need to remain with the company for at least that long to get your money's worth, as the vesting schedule would dictate when you can access the full value of your stocks.

Sources:
[1] https://www.randstadusa.com/job-seeker/career-advice/salary/how-to-negotiate-benefits-package/

**Sources Cited:**
• https://anderscpa.com/learn/blog/understanding-employee-benefits-guide-for-recent-graduates/
• https://www.randstadusa.com/job-seeker/career-advice/salary/how-to-negotiate-benefits-package/

#### Q3: If I am already covered for health insurance, should I even consider enrolling in my company's plan?

**Expected:**
> Yes, you should consider enrolling in your company's plan because employer plans typically offer better coverage and lower costs than individual plans, plus employers often contribute to premiums, deductibles, or HSA/FSA accounts. You may also face coordination-of-benefits questions and tax implications.

**System Response:**
> I don't have enough information in my sources to answer that accurately. I recommend checking your company's HR portal or benefits handbook.

Sources:
[1] https://www.cigna.com/knowledge-center/hdhp-vs-ppo-plans
[2] https://anderscpa.com/learn/blog/understanding-employee-benefits-guide-for-recent-graduates/
[3] https://anderscpa.com/learn/blog/understanding-employee-benefits-guide-for-recent-graduates/

**Sources Cited:**
• https://anderscpa.com/learn/blog/understanding-employee-benefits-guide-for-recent-graduates/
• https://www.cigna.com/knowledge-center/hdhp-vs-ppo-plans

#### Q4: What is open enrollment?

**Expected:**
> Open enrollment is the annual period (typically once per year, often in the fall) when employees can enroll in, change, or drop their benefits plans. Outside of open enrollment, you can only change elections if you experience a qualifying life event (marriage, birth, job loss, etc.).

**System Response:**
> Open enrollment is the annual time period when employees can enroll in benefits for the next year. If employees do not elect certain benefits at the time of hire or during open enrollment, then there are other events that can occur to qualify an individual to enroll at that time, such as turning 26, a change in family situation, or if a spouse loses their group benefits.

Sources:
[1] https://anderscpa.com/learn/blog/understanding-employee-benefits-guide-for-recent-graduates/
[2] https://anderscpa.com/learn/blog/understanding-employee-benefits-guide-for-recent-graduates/

**Sources Cited:**
• https://anderscpa.com/learn/blog/understanding-employee-benefits-guide-for-recent-graduates/

#### Q5: What is the difference between PTO, short-term disability, and long-term disability?

**Expected:**
> PTO (paid time off) covers vacation, sick days, and personal days that you can use at your discretion. Short-term disability replaces a portion of your salary when a medical issue prevents you from working, typically lasting weeks to months. Long-term disability replaces a portion of salary for longer absences, starting when short-term disability ends and potentially lasting until retirement.

**System Response:**
> According to the context, the main difference between PTO, short-term disability, and long-term disability is the purpose and duration of each benefit.

PTO (Paid Time Off) includes personal days, sick days, and vacation days that employees can use for various purposes, and the amount of PTO varies among employers.

Short-term disability insurance is used when a medical issue prevents an employee from working, and it provides a portion of their salary while they are out of work.

Long-term disability insurance typically starts when the short-term disability ends, and it also provides a portion of the employee's salary while they are unable to work due to a medical issue.

In summary, PTO is for general time off, while short-term and long-term disability insurance are for extended periods of time when an employee is unable to work due to a medical issue.

Sources:
[1] https://anderscpa.com/learn/blog/understanding-employee-benefits-guide-for-recent-graduates/

**Sources Cited:**
• https://anderscpa.com/learn/blog/understanding-employee-benefits-guide-for-recent-graduates/
• https://www.dol.gov/agencies/ebsa/about-ebsa/our-activities/resource-center/publications/filing-a-claim-for-your-health-benefits

#### Q6: What is the advantage of using commuter benefits instead of paying for transit or parking out of pocket?

**Expected:**
> Commuter benefits allow you to pay for public transit, parking, or vanpool costs with pre-tax dollars, reducing your taxable income and saving on taxes. Unlike medical FSAs, commuter benefit plans often allow unused funds to roll over to the next year (check your plan), making them a lower-risk savings option for predictable commuting costs.

**System Response:**
> I don't have enough information in my sources to answer that accurately. I recommend checking your company's HR portal or benefits handbook.

Sources:
[1] https://anderscpa.com/learn/blog/understanding-employee-benefits-guide-for-recent-graduates/
[2] https://anderscpa.com/learn/blog/understanding-employee-benefits-guide-for-recent-graduates/
[3] https://anderscpa.com/learn/blog/understanding-employee-benefits-guide-for-recent-graduates/ 

Note: The context provided does not mention commuter benefits or the advantages of using them. It discusses other benefits such as flexible schedules, paid parking, and health insurance plans.

**Sources Cited:**
• https://anderscpa.com/learn/blog/understanding-employee-benefits-guide-for-recent-graduates/


## Run #2 — 2026-06-07 22:28:25

### Corpus Status
- **Total chunks:** 60
- **Sources ingested:** 9
- **Sources breakdown:**
  - `7` chunks from https://anderscpa.com/learn/blog/understanding-employee-bene...
  - `5` chunks from https://turbotax.intuit.com/tax-tips/jobs-and-career/guide-t...
  - `6` chunks from https://www.cigna.com/knowledge-center/hdhp-vs-ppo-plans...
  - `15` chunks from https://www.dol.gov/agencies/ebsa/about-ebsa/our-activities/...
  - `2` chunks from https://www.dol.gov/general/topic/health-plans/erisa...
  - `5` chunks from https://www.fhb.com/en/resource-center/life-stages/workplace...
  - `3` chunks from https://www.metlife.com/stories/benefits/hdhp-vs-ppo/...
  - `7` chunks from https://www.randstadusa.com/job-seeker/career-advice/salary/...
  - `10` chunks from https://www.wovencapital.net/how-to-evaluate-equity-compensa...

### Changes Since Last Run
Added trafilatura and readability-lxml extraction libraries. Improved extraction pipeline now tries multiple methods (trafilatura → readability → BeautifulSoup). Successfully recovered 3 previously blocked sources: MetLife, FHB, Woven Capital. Corpus expanded from 40 to 60 chunks (50% improvement). Reddit still blocked (9/10 sources now working).

### Evaluation Results

#### Q1: Why should someone choose to max out their medical FSA account?

**Expected:**
> You should max out your medical FSA only if you have predictable medical expenses (prescriptions, glasses, copays) that you'll incur within the plan year, because contributions are pre-tax. However, medical FSAs have a strict 'use it or lose it' rule—unused money is forfeited (though some employers allow a small grace period or up to $610 carryover in 2026)—so you shouldn't max out if you're uncertain about expenses.

**System Response:**
> According to the context, someone should consider maxing out their medical FSA account if they have regular medical expenses, such as prescriptions, glasses, or planned procedures. This is because the money in an FSA can be used for qualified medical expenses, and contributions are made with pre-tax dollars, providing tax benefits. However, it's essential to estimate annual medical expenses realistically, as any unused funds in the FSA will be lost at the end of the year due to the "use it or lose it" provision.

Sources:
[1] https://turbotax.intuit.com/tax-tips/jobs-and-career/guide-to-your-employers-benefits-programs-tax-wise-401k-matching-hsas-flexible-etc/L74Iljjyz
[2] https://anderscpa.com/learn/blog/understanding-employee-benefits-guide-for-recent-graduates/
[3] https://www.fhb.com/en/resource-center/life-stages/workplace-financial-benefits-a-beginners-guide

**Sources Cited:**
• https://anderscpa.com/learn/blog/understanding-employee-benefits-guide-for-recent-graduates/
• https://turbotax.intuit.com/tax-tips/jobs-and-career/guide-to-your-employers-benefits-programs-tax-wise-401k-matching-hsas-flexible-etc/L74Iljjyz
• https://www.fhb.com/en/resource-center/life-stages/workplace-financial-benefits-a-beginners-guide

#### Q2: If my stocks at a company mature only after 5 years, do I need to remain with the company to get my money's worth?

**Expected:**
> Yes, you must remain with the company until the shares vest (mature). If you leave before 5 years, unvested shares are forfeited and you lose that equity compensation. However, once shares vest and are delivered to you, you own them and they can't be clawed back if you leave.

**System Response:**
> According to the context, the typical vesting schedule for equity is 4 years, with a 1-year cliff. However, it does not specifically mention a 5-year vesting schedule. But, based on the information provided, it can be inferred that if your stocks mature only after 5 years, you would likely need to remain with the company for at least 5 years to fully vest and receive the value of your equity grant.

Sources:
[1] https://www.wovencapital.net/how-to-evaluate-equity-compensation-in-your-first-tech-job-offer-rsus-stock-options-and-vesting-schedules-explained/
[2] https://www.wovencapital.net/how-to-evaluate-equity-compensation-in-your-first-tech-job-offer-rsus-stock-options-and-vesting-schedules-explained/

**Sources Cited:**
• https://www.wovencapital.net/how-to-evaluate-equity-compensation-in-your-first-tech-job-offer-rsus-stock-options-and-vesting-schedules-explained/

#### Q3: If I am already covered for health insurance, should I even consider enrolling in my company's plan?

**Expected:**
> Yes, you should consider enrolling in your company's plan because employer plans typically offer better coverage and lower costs than individual plans, plus employers often contribute to premiums, deductibles, or HSA/FSA accounts. You may also face coordination-of-benefits questions and tax implications.

**System Response:**
> I don't have enough information in my sources to answer that accurately. I recommend checking your company's HR portal or benefits handbook.

Sources:
[1] https://www.fhb.com/en/resource-center/life-stages/workplace-financial-benefits-a-beginners-guide
[2] https://www.cigna.com/knowledge-center/hdhp-vs-ppo-plans
[3] https://anderscpa.com/learn/blog/understanding-employee-benefits-guide-for-recent-graduates/

**Sources Cited:**
• https://anderscpa.com/learn/blog/understanding-employee-benefits-guide-for-recent-graduates/
• https://www.cigna.com/knowledge-center/hdhp-vs-ppo-plans
• https://www.fhb.com/en/resource-center/life-stages/workplace-financial-benefits-a-beginners-guide

#### Q4: What is open enrollment?

**Expected:**
> Open enrollment is the annual period (typically once per year, often in the fall) when employees can enroll in, change, or drop their benefits plans. Outside of open enrollment, you can only change elections if you experience a qualifying life event (marriage, birth, job loss, etc.).

**System Response:**
> Open enrollment is the annual time period when employees can enroll in benefits for the next year. If employees do not elect certain benefits at the time of hire or during open enrollment, they may still be able to enroll outside of this period if certain events occur, such as turning 26, a change in family situation, or if a spouse loses their group benefits.

Sources:
[2] https://anderscpa.com/learn/blog/understanding-employee-benefits-guide-for-recent-graduates/

**Sources Cited:**
• https://anderscpa.com/learn/blog/understanding-employee-benefits-guide-for-recent-graduates/

#### Q5: What is the difference between PTO, short-term disability, and long-term disability?

**Expected:**
> PTO (paid time off) covers vacation, sick days, and personal days that you can use at your discretion. Short-term disability replaces a portion of your salary when a medical issue prevents you from working, typically lasting weeks to months. Long-term disability replaces a portion of salary for longer absences, starting when short-term disability ends and potentially lasting until retirement.

**System Response:**
> According to the context, Paid Time Off (PTO) includes personal days, sick days, and vacation days that employees accrue over time, and the amount of PTO varies among employers. 

Short-term disability, on the other hand, is a type of insurance that provides a portion of an employee's salary when a medical issue prevents them from working. 

Long-term disability typically starts when the short-term disability ends, and it also provides a portion of an employee's salary when they are unable to work due to a medical issue.

In summary, PTO is time off that employees can take for various reasons, while short-term and long-term disability are types of insurance that provide income replacement when an employee is unable to work due to a medical issue.

Sources:
[1] https://anderscpa.com/learn/blog/understanding-employee-benefits-guide-for-recent-graduates/

**Sources Cited:**
• https://anderscpa.com/learn/blog/understanding-employee-benefits-guide-for-recent-graduates/
• https://www.cigna.com/knowledge-center/hdhp-vs-ppo-plans

#### Q6: What is the advantage of using commuter benefits instead of paying for transit or parking out of pocket?

**Expected:**
> Commuter benefits allow you to pay for public transit, parking, or vanpool costs with pre-tax dollars, reducing your taxable income and saving on taxes. Unlike medical FSAs, commuter benefit plans often allow unused funds to roll over to the next year (check your plan), making them a lower-risk savings option for predictable commuting costs.

**System Response:**
> I don't have enough information in my sources to answer that accurately. I recommend checking your company's HR portal or benefits handbook.

Sources:
[1] https://anderscpa.com/learn/blog/understanding-employee-benefits-guide-for-recent-graduates/
[2] https://turbotax.intuit.com/tax-tips/jobs-and-career/guide-to-your-employers-benefits-programs-tax-wise-401k-matching-hsas-flexible-etc/L74Iljjyz
[3] https://www.randstadusa.com/job-seeker/career-advice/salary/how-to-negotiate-benefits-package/

**Sources Cited:**
• https://anderscpa.com/learn/blog/understanding-employee-benefits-guide-for-recent-graduates/
• https://turbotax.intuit.com/tax-tips/jobs-and-career/guide-to-your-employers-benefits-programs-tax-wise-401k-matching-hsas-flexible-etc/L74Iljjyz
• https://www.randstadusa.com/job-seeker/career-advice/salary/how-to-negotiate-benefits-package/


## Run #3 — 2026-06-07 22:31:40

### Corpus Status
- **Total chunks:** 101
- **Sources ingested:** 14
- **Sources breakdown:**
  - `7` chunks from https://anderscpa.com/learn/blog/understanding-employee-bene...
  - `7` chunks from https://getbenepass.com/blog/pre-tax-commuter-benefits...
  - `8` chunks from https://livelyme.com/blog/pre-tax-commuter-benefit-contribut...
  - `6` chunks from https://thatch.com/blog/opting-out-employer-health-insurance...
  - `5` chunks from https://turbotax.intuit.com/tax-tips/jobs-and-career/guide-t...
  - `6` chunks from https://www.cigna.com/knowledge-center/hdhp-vs-ppo-plans...
  - `18` chunks from https://www.deel.com/blog/types-of-employee-benefits/...
  - `15` chunks from https://www.dol.gov/agencies/ebsa/about-ebsa/our-activities/...
  - `2` chunks from https://www.dol.gov/general/topic/health-plans/erisa...
  - `5` chunks from https://www.fhb.com/en/resource-center/life-stages/workplace...
  - `2` chunks from https://www.healthcare.gov/have-job-based-coverage/...
  - `3` chunks from https://www.metlife.com/stories/benefits/hdhp-vs-ppo/...
  - `7` chunks from https://www.randstadusa.com/job-seeker/career-advice/salary/...
  - `10` chunks from https://www.wovencapital.net/how-to-evaluate-equity-compensa...

### Changes Since Last Run
Added 5 new sources focused on commuter benefits and enrollment decisions: Lively, GetBenepass, Healthcare.gov, Thatch, Deel. Corpus expanded from 60 to 101 chunks (68% increase). Expected to improve Q3 (company plan) and Q6 (commuter benefits) answers while maintaining quality of Q1-Q5. Now have 14/15 sources working (Reddit still blocked).

### Evaluation Results

#### Q1: Why should someone choose to max out their medical FSA account?

**Expected:**
> You should max out your medical FSA only if you have predictable medical expenses (prescriptions, glasses, copays) that you'll incur within the plan year, because contributions are pre-tax. However, medical FSAs have a strict 'use it or lose it' rule—unused money is forfeited (though some employers allow a small grace period or up to $610 carryover in 2026)—so you shouldn't max out if you're uncertain about expenses.

**System Response:**
> According to the context, there isn't a direct statement on why someone should choose to max out their medical FSA account. However, it's mentioned that an FSA provides tax benefits as the money contributed comes out of your paycheck before you pay tax on it, and it can be used for medical expenses not covered by insurance, such as dental or vision expenses. 

It's also worth noting that there's a 'use it or lose it' provision, meaning any money in your FSA that you don't spend by the end of the year will be lost. So, it might be beneficial to contribute to an FSA if you have predictable medical expenses that aren't covered by your insurance, but you should be careful not to over-contribute.

Sources:
[1] https://turbotax.intuit.com/tax-tips/jobs-and-career/guide-to-your-employers-benefits-programs-tax-wise-401k-matching-hsas-flexible-etc/L74Iljjyz
[2] https://anderscpa.com/learn/blog/understanding-employee-benefits-guide-for-recent-graduates/

**Sources Cited:**
• https://anderscpa.com/learn/blog/understanding-employee-benefits-guide-for-recent-graduates/
• https://turbotax.intuit.com/tax-tips/jobs-and-career/guide-to-your-employers-benefits-programs-tax-wise-401k-matching-hsas-flexible-etc/L74Iljjyz
• https://www.deel.com/blog/types-of-employee-benefits/

#### Q2: If my stocks at a company mature only after 5 years, do I need to remain with the company to get my money's worth?

**Expected:**
> Yes, you must remain with the company until the shares vest (mature). If you leave before 5 years, unvested shares are forfeited and you lose that equity compensation. However, once shares vest and are delivered to you, you own them and they can't be clawed back if you leave.

**System Response:**
> According to the context, the typical vesting schedule for equity is 4 years, with a 1-year cliff. This means that you don't get any equity in the first year, and then 25% of your grant vests all at once on your 1-year anniversary. The remaining 75% vests gradually over the next 3 years. However, your question mentions a 5-year maturity period, which is not explicitly discussed in the context.

Since the context only discusses 4-year vesting schedules, I don't have enough information to accurately answer your question about a 5-year maturity period. 

Sources:
[1] https://www.wovencapital.net/how-to-evaluate-equity-compensation-in-your-first-tech-job-offer-rsus-stock-options-and-vesting-schedules-explained/
[2] https://www.wovencapital.net/how-to-evaluate-equity-compensation-in-your-first-tech-job-offer-rsus-stock-options-and-vesting-schedules-explained/
[3] https://www.wovencapital.net/how-to-evaluate-equity-compensation-in-your-first-tech-job-offer-rsus-stock-options-and-vesting-schedules-explained/

**Sources Cited:**
• https://www.wovencapital.net/how-to-evaluate-equity-compensation-in-your-first-tech-job-offer-rsus-stock-options-and-vesting-schedules-explained/

#### Q3: If I am already covered for health insurance, should I even consider enrolling in my company's plan?

**Expected:**
> Yes, you should consider enrolling in your company's plan because employer plans typically offer better coverage and lower costs than individual plans, plus employers often contribute to premiums, deductibles, or HSA/FSA accounts. You may also face coordination-of-benefits questions and tax implications.

**System Response:**
> If you're already covered for health insurance, it might not be necessary to enroll in your company's plan. According to the sources, some employees choose to waive coverage because they're already covered under a spouse's or partner's employer plan, which may offer better networks or lower costs. However, before making a decision, consider the potential risks, such as losing employer contributions and tax implications. It's essential to weigh the costs and benefits of your current coverage against the company's plan to determine which option is more suitable for you.

Sources:
[1] https://thatch.com/blog/opting-out-employer-health-insurance-special-considerations
[2] https://thatch.com/blog/opting-out-employer-health-insurance-special-considerations
[3] https://thatch.com/blog/opting-out-employer-health-insurance-special-considerations

**Sources Cited:**
• https://thatch.com/blog/opting-out-employer-health-insurance-special-considerations

#### Q4: What is open enrollment?

**Expected:**
> Open enrollment is the annual period (typically once per year, often in the fall) when employees can enroll in, change, or drop their benefits plans. Outside of open enrollment, you can only change elections if you experience a qualifying life event (marriage, birth, job loss, etc.).

**System Response:**
> I don't have enough information in my sources to answer that accurately. I recommend checking your company's HR portal or benefits handbook.

Sources:
[1] https://anderscpa.com/learn/blog/understanding-employee-benefits-guide-for-recent-graduates/
[2] https://thatch.com/blog/opting-out-employer-health-insurance-special-considerations 
[3] https://thatch.com/blog/opting-out-employer-health-insurance-special-considerations 

Note: Although the term "open enrollment" is mentioned in source [2], it is not explicitly defined in the provided context.

**Sources Cited:**
• https://anderscpa.com/learn/blog/understanding-employee-benefits-guide-for-recent-graduates/
• https://thatch.com/blog/opting-out-employer-health-insurance-special-considerations

#### Q5: What is the difference between PTO, short-term disability, and long-term disability?

**Expected:**
> PTO (paid time off) covers vacation, sick days, and personal days that you can use at your discretion. Short-term disability replaces a portion of your salary when a medical issue prevents you from working, typically lasting weeks to months. Long-term disability replaces a portion of salary for longer absences, starting when short-term disability ends and potentially lasting until retirement.

**System Response:**
> According to the context, PTO (Paid Time Off) includes personal days, sick days, and vacation days that employees can use for rest and recovery. The amount of PTO varies among employers and can be accrued over time.

Short-term disability, on the other hand, is a type of insurance that provides a portion of an employee's salary when a medical issue prevents them from working. 

Long-term disability typically starts when the short-term disability ends, and it also provides a portion of an employee's salary when a medical issue prevents them from working.

So, the main difference between PTO, short-term disability, and long-term disability is that PTO is used for planned or unplanned time off, such as vacations or sick days, while short-term and long-term disability are used when an employee is unable to work due to a medical issue.

Sources:
[1] https://anderscpa.com/learn/blog/understanding-employee-benefits-guide-for-recent-graduates/
[3] https://www.deel.com/blog/types-of-employee-benefits/

**Sources Cited:**
• https://anderscpa.com/learn/blog/understanding-employee-benefits-guide-for-recent-graduates/
• https://www.deel.com/blog/types-of-employee-benefits/

#### Q6: What is the advantage of using commuter benefits instead of paying for transit or parking out of pocket?

**Expected:**
> Commuter benefits allow you to pay for public transit, parking, or vanpool costs with pre-tax dollars, reducing your taxable income and saving on taxes. Unlike medical FSAs, commuter benefit plans often allow unused funds to roll over to the next year (check your plan), making them a lower-risk savings option for predictable commuting costs.

**System Response:**
> The advantage of using commuter benefits is that it can help reduce the cost-burden of commuting expenses for employees. With pre-tax commuter benefits, employees can contribute money to their account on a monthly basis without paying taxes on it, leading to savings on their income taxes. This means that employees can take home more of the money they earn. Additionally, businesses also save money on their payroll taxes when they offer pre-tax benefits.

Sources:
[1] https://livelyme.com/blog/pre-tax-commuter-benefit-contribution-limits
[2] https://livelyme.com/blog/pre-tax-commuter-benefit-contribution-limits
[3] https://getbenepass.com/blog/pre-tax-commuter-benefits

**Sources Cited:**
• https://getbenepass.com/blog/pre-tax-commuter-benefits
• https://livelyme.com/blog/pre-tax-commuter-benefit-contribution-limits


## Run #4 — 2026-06-07 22:33:45

### Corpus Status
- **Total chunks:** 101
- **Sources ingested:** 14
- **Sources breakdown:**
  - `7` chunks from https://anderscpa.com/learn/blog/understanding-employee-bene...
  - `7` chunks from https://getbenepass.com/blog/pre-tax-commuter-benefits...
  - `8` chunks from https://livelyme.com/blog/pre-tax-commuter-benefit-contribut...
  - `6` chunks from https://thatch.com/blog/opting-out-employer-health-insurance...
  - `5` chunks from https://turbotax.intuit.com/tax-tips/jobs-and-career/guide-t...
  - `6` chunks from https://www.cigna.com/knowledge-center/hdhp-vs-ppo-plans...
  - `18` chunks from https://www.deel.com/blog/types-of-employee-benefits/...
  - `15` chunks from https://www.dol.gov/agencies/ebsa/about-ebsa/our-activities/...
  - `2` chunks from https://www.dol.gov/general/topic/health-plans/erisa...
  - `5` chunks from https://www.fhb.com/en/resource-center/life-stages/workplace...
  - `2` chunks from https://www.healthcare.gov/have-job-based-coverage/...
  - `3` chunks from https://www.metlife.com/stories/benefits/hdhp-vs-ppo/...
  - `7` chunks from https://www.randstadusa.com/job-seeker/career-advice/salary/...
  - `10` chunks from https://www.wovencapital.net/how-to-evaluate-equity-compensa...

### Changes Since Last Run
Increased top-k from 3 to 5 to reduce retrieval noise in larger corpus (101 chunks). Expected to recover answers for Q1, Q2, Q4 that regressed in Run #3, while maintaining fixes for Q3 and Q6.

### Evaluation Results

#### Q1: Why should someone choose to max out their medical FSA account?

**Expected:**
> You should max out your medical FSA only if you have predictable medical expenses (prescriptions, glasses, copays) that you'll incur within the plan year, because contributions are pre-tax. However, medical FSAs have a strict 'use it or lose it' rule—unused money is forfeited (though some employers allow a small grace period or up to $610 carryover in 2026)—so you shouldn't max out if you're uncertain about expenses.

**System Response:**
> According to the context, someone should choose to max out their medical FSA account if they have regular medical expenses, such as prescriptions, glasses, or planned procedures. This is because an FSA allows you to set aside pre-tax money for medical expenses, which can provide up to 30% savings on out-of-pocket healthcare expenses. However, it's also important to note that if you don't use the money in your FSA by the end of the year, you'll lose it, so it's essential to estimate your annual medical expenses realistically before contributing to an FSA.

Sources:
[1] https://turbotax.intuit.com/tax-tips/jobs-and-career/guide-to-your-employers-benefits-programs-tax-wise-401k-matching-hsas-flexible-etc/L74Iljjyz
[2] https://anderscpa.com/learn/blog/understanding-employee-benefits-guide-for-recent-graduates/
[4] https://www.fhb.com/en/resource-center/life-stages/workplace-financial-benefits-a-beginners-guide

**Sources Cited:**
• https://anderscpa.com/learn/blog/understanding-employee-benefits-guide-for-recent-graduates/
• https://livelyme.com/blog/pre-tax-commuter-benefit-contribution-limits
• https://turbotax.intuit.com/tax-tips/jobs-and-career/guide-to-your-employers-benefits-programs-tax-wise-401k-matching-hsas-flexible-etc/L74Iljjyz
• https://www.deel.com/blog/types-of-employee-benefits/
• https://www.fhb.com/en/resource-center/life-stages/workplace-financial-benefits-a-beginners-guide

#### Q2: If my stocks at a company mature only after 5 years, do I need to remain with the company to get my money's worth?

**Expected:**
> Yes, you must remain with the company until the shares vest (mature). If you leave before 5 years, unvested shares are forfeited and you lose that equity compensation. However, once shares vest and are delivered to you, you own them and they can't be clawed back if you leave.

**System Response:**
> According to the context, if you have a typical vesting schedule, such as a "four-year vest with a one-year cliff," you would need to stay with the company for at least a year to start receiving your equity. However, since your specific situation mentions a 5-year maturity period, which is not explicitly discussed in the context, I can only provide general information.

Typically, equity compensation, such as RSUs or stock options, vests over time, and you would need to be with the company to receive the full value of your grant. If you leave the company before your equity is fully vested, you might walk away with unvested equity, which could be worth tens of thousands of dollars.

To get a clear answer, I would recommend checking your company's specific vesting schedule and equity incentive plan document, as the context suggests that vesting schedules can vary.

Sources:
[1] https://www.wovencapital.net/how-to-evaluate-equity-compensation-in-your-first-tech-job-offer-rsus-stock-options-and-vesting-schedules-explained/
[2] https://www.wovencapital.net/how-to-evaluate-equity-compensation-in-your-first-tech-job-offer-rsus-stock-options-and-vesting-schedules-explained/

**Sources Cited:**
• https://www.wovencapital.net/how-to-evaluate-equity-compensation-in-your-first-tech-job-offer-rsus-stock-options-and-vesting-schedules-explained/

#### Q3: If I am already covered for health insurance, should I even consider enrolling in my company's plan?

**Expected:**
> Yes, you should consider enrolling in your company's plan because employer plans typically offer better coverage and lower costs than individual plans, plus employers often contribute to premiums, deductibles, or HSA/FSA accounts. You may also face coordination-of-benefits questions and tax implications.

**System Response:**
> If you're already covered for health insurance, you may not need to enroll in your company's plan. According to the sources, many employees opt out of employer-sponsored coverage because they're already covered under a spouse's or partner's plan, which may offer better networks or lower costs. However, before making a decision, consider the potential loss of employer contributions, tax implications, and coverage gaps. You should also verify that your alternative coverage is ACA-compliant and comprehensive.

Sources:
[1] https://thatch.com/blog/opting-out-employer-health-insurance-special-considerations
[2] https://thatch.com/blog/opting-out-employer-health-insurance-special-considerations
[3] https://thatch.com/blog/opting-out-employer-health-insurance-special-considerations
[4] https://thatch.com/blog/opting-out-employer-health-insurance-special-considerations
[5] https://thatch.com/blog/opting-out-employer-health-insurance-special-considerations

**Sources Cited:**
• https://thatch.com/blog/opting-out-employer-health-insurance-special-considerations

#### Q4: What is open enrollment?

**Expected:**
> Open enrollment is the annual period (typically once per year, often in the fall) when employees can enroll in, change, or drop their benefits plans. Outside of open enrollment, you can only change elections if you experience a qualifying life event (marriage, birth, job loss, etc.).

**System Response:**
> Open enrollment is the annual time period when employees can enroll in benefits for the next year. If employees do not elect certain benefits at the time of hire or during open enrollment, then there are other events that can occur that can qualify an individual to enroll at that time, such as turning 26, a change in family situation, or if a spouse loses their group benefits.

Sources:
[4] https://anderscpa.com/learn/blog/understanding-employee-benefits-guide-for-recent-graduates/

**Sources Cited:**
• https://anderscpa.com/learn/blog/understanding-employee-benefits-guide-for-recent-graduates/
• https://thatch.com/blog/opting-out-employer-health-insurance-special-considerations

#### Q5: What is the difference between PTO, short-term disability, and long-term disability?

**Expected:**
> PTO (paid time off) covers vacation, sick days, and personal days that you can use at your discretion. Short-term disability replaces a portion of your salary when a medical issue prevents you from working, typically lasting weeks to months. Long-term disability replaces a portion of salary for longer absences, starting when short-term disability ends and potentially lasting until retirement.

**System Response:**
> PTO (Paid Time Off) includes personal days, sick days, and vacation days that employees can use for rest and recovery. The amount of PTO varies among employers and can be accrued over time.

Short-term disability, on the other hand, is a type of insurance that provides a portion of an employee's salary when a medical issue prevents them from working. 

Long-term disability typically starts when the short-term disability ends, and it also provides a portion of an employee's salary while they are unable to work due to a medical issue.

In summary, PTO is for planned or unplanned time off, while short-term and long-term disability are for periods when an employee is unable to work due to a medical issue.

Sources:
[1] https://anderscpa.com/learn/blog/understanding-employee-benefits-guide-for-recent-graduates/
[3] https://www.deel.com/blog/types-of-employee-benefits/

**Sources Cited:**
• https://anderscpa.com/learn/blog/understanding-employee-benefits-guide-for-recent-graduates/
• https://www.cigna.com/knowledge-center/hdhp-vs-ppo-plans
• https://www.deel.com/blog/types-of-employee-benefits/

#### Q6: What is the advantage of using commuter benefits instead of paying for transit or parking out of pocket?

**Expected:**
> Commuter benefits allow you to pay for public transit, parking, or vanpool costs with pre-tax dollars, reducing your taxable income and saving on taxes. Unlike medical FSAs, commuter benefit plans often allow unused funds to roll over to the next year (check your plan), making them a lower-risk savings option for predictable commuting costs.

**System Response:**
> The advantage of using commuter benefits instead of paying for transit or parking out of pocket is that it allows employees to save money on their commuting expenses. With pre-tax commuter benefits, employees can contribute to their accounts on a tax-free basis, which means they don't have to pay income taxes on the money they set aside for commuting. This can lead to significant savings, as employees can contribute up to $3,780 annually toward transportation costs and another $3,780 toward parking tax-free. 

Sources:
[1] https://livelyme.com/blog/pre-tax-commuter-benefit-contribution-limits
[2] https://livelyme.com/blog/pre-tax-commuter-benefit-contribution-limits
[3] https://getbenepass.com/blog/pre-tax-commuter-benefits
[4] https://getbenepass.com/blog/pre-tax-commuter-benefits
[5] https://getbenepass.com/blog/pre-tax-commuter-benefits

**Sources Cited:**
• https://getbenepass.com/blog/pre-tax-commuter-benefits
• https://livelyme.com/blog/pre-tax-commuter-benefit-contribution-limits

