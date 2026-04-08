"""
Golden Dataset — 50 Expert-Crafted Q&A Pairs for UK Financial Compliance.

Covers:
  - FCA Handbook & Principles (PRIN, SYSC, COBS, MCOB)
  - MiFID II / MiFIR
  - Senior Managers & Certification Regime (SMCR)
  - Consumer Duty (PS22/9)
  - Anti-Money Laundering (AML) / KYC
  - Sanctions Screening
  - Market Abuse Regulation (MAR)
  - PRIIPs / KID requirements
  - GDPR in Financial Services
  - Whistleblowing (SYSC 18)
  - Capital Adequacy / Prudential Standards
  - Operational Resilience (PS21/3)
"""


def get_golden_dataset() -> list[dict]:
    """
    Return 50 complex questions with ground-truth answers for evaluating
    a UK financial compliance RAG pipeline.
    
    Each entry: {"question": str, "ground_truth": str}
    """
    return [
        # ── FCA Principles & Handbook ─────────────────────────────────────
        {
            "question": "What are the FCA's 12 Principles for Businesses and how do they apply to regulated firms?",
            "ground_truth": (
                "The FCA's 12 Principles for Businesses (PRIN 2.1) are fundamental obligations for all regulated firms. "
                "They include: (1) Integrity, (2) Skill, care and diligence, (3) Management and control, "
                "(4) Financial prudence, (5) Market conduct, (6) Customers' interests, (7) Communications with clients, "
                "(8) Conflicts of interest, (9) Customers: relationships of trust, (10) Clients' assets, "
                "(11) Relations with regulators, (12) Consumer Duty. These principles form the bedrock of "
                "FCA regulation and breaches can result in enforcement action including fines and prohibition orders."
            ),
        },
        {
            "question": "How does the FCA Threshold Conditions framework determine whether a firm should be authorised?",
            "ground_truth": (
                "The FCA Threshold Conditions (COND) are the minimum requirements a firm must meet to be "
                "authorised and to continue carrying on regulated activities. They include: adequate resources "
                "(financial and non-financial), suitability (competent and prudent management, business model), "
                "effective supervision capability, and appropriate non-financial resources including IT systems "
                "and compliance infrastructure. Firms must satisfy these conditions on an ongoing basis."
            ),
        },
        {
            "question": "What is the difference between COBS rules and MCOB rules in the FCA Handbook?",
            "ground_truth": (
                "COBS (Conduct of Business Sourcebook) governs the conduct of firms providing investment "
                "services, including client communication, suitability assessments, best execution, and "
                "inducements. MCOB (Mortgages and Home Finance: Conduct of Business) specifically governs "
                "firms that advise on, sell, or administer mortgages and home finance products. MCOB includes "
                "rules on responsible lending, affordability assessments, and mortgage disclosure requirements. "
                "The key distinction is the product set covered — COBS for investments, MCOB for mortgages."
            ),
        },
        {
            "question": "Explain the FCA's approach to proportionality in financial regulation.",
            "ground_truth": (
                "The FCA applies proportionality by tailoring regulatory requirements to the size, nature, "
                "scale, and complexity of a firm's activities. Smaller firms may face lighter regulatory "
                "burdens in areas like reporting frequency and governance structure, while systemically "
                "important firms face enhanced requirements. This principle is embedded in SYSC (Senior "
                "Management Arrangements, Systems and Controls) and ensures regulation is not unduly "
                "burdensome while maintaining consumer and market protection."
            ),
        },
        {
            "question": "What are the FCA's requirements for handling client complaints under DISP?",
            "ground_truth": (
                "Under DISP (Dispute Resolution: Complaints), firms must have effective complaints handling "
                "procedures. Key requirements include: acknowledging complaints promptly, investigating "
                "competently and impartially, offering redress where appropriate, providing a final response "
                "within 8 weeks (or 15 business days for payment services), informing clients of their right "
                "to refer to the Financial Ombudsman Service (FOS), maintaining complaints records, and "
                "reporting complaints data to the FCA in the bi-annual return."
            ),
        },

        # ── MiFID II / MiFIR ──────────────────────────────────────────────
        {
            "question": "What are the key best execution obligations under MiFID II for investment firms?",
            "ground_truth": (
                "Under MiFID II Article 27, investment firms must take all sufficient steps to obtain the "
                "best possible result for clients (best execution) considering price, costs, speed, likelihood "
                "of execution and settlement, size, nature, and any other relevant consideration. Firms must "
                "establish an order execution policy, obtain client consent, monitor effectiveness of execution "
                "arrangements, publish top-5 execution venue reports (RTS 28), and review the policy at least "
                "annually. The obligation applies differently for professional and retail clients."
            ),
        },
        {
            "question": "How does MiFID II regulate the provision of investment research and inducements?",
            "ground_truth": (
                "MiFID II introduced strict rules on investment research (Article 24). Firms must either "
                "pay for research from their own resources (P&L) or through a Research Payment Account (RPA) "
                "funded by client commissions with explicit budgets and client disclosure. Research must not "
                "be treated as an inducement. These 'unbundling' rules aim to prevent conflicts of interest "
                "and improve transparency. Minor non-monetary benefits are exempt under certain conditions."
            ),
        },
        {
            "question": "What transaction reporting obligations does MiFIR impose and what data must be included?",
            "ground_truth": (
                "Under MiFIR Article 26, investment firms must report complete and accurate details of "
                "transactions in financial instruments to competent authorities no later than T+1. Reports "
                "must include 65 fields covering: instrument identification (ISIN), client identification "
                "(LEI for legal entities, national ID for individuals), decision-maker details, execution "
                "details (price, quantity, venue), timestamps, and the firm's own LEI. Reports can be "
                "submitted directly to the National Competent Authority or through an Approved Reporting "
                "Mechanism (ARM)."
            ),
        },
        {
            "question": "Explain the MiFID II product governance requirements for manufacturers and distributors.",
            "ground_truth": (
                "MiFID II product governance (Article 16(3) and 24(2)) requires manufacturers to: define "
                "a target market for each product, conduct scenario analysis, perform product testing before "
                "launch, and review products throughout their lifecycle. Distributors must: understand the "
                "products they offer, assess compatibility with their clients' needs, identify the target "
                "market, and provide feedback to manufacturers. Both must maintain records and ensure products "
                "are distributed appropriately within the identified target market."
            ),
        },
        {
            "question": "What are the MiFID II requirements for algorithmic and high-frequency trading firms?",
            "ground_truth": (
                "MiFID II (Articles 17, 48) requires algorithmic trading firms to: implement effective "
                "systems and risk controls, have business continuity arrangements, test algorithms thoroughly, "
                "include circuit breakers (kill switches), maintain records of all orders (including cancelled), "
                "notify the competent authority and trading venue. High-frequency traders must additionally: "
                "store accurate, timestamped records of all placed orders, register as investment firms (unless "
                "exempt), and be subject to specific fee structures by venues to discourage excessive orders."
            ),
        },

        # ── SMCR ──────────────────────────────────────────────────────────
        {
            "question": "What is the Senior Managers and Certification Regime (SMCR) and who does it apply to?",
            "ground_truth": (
                "The SMCR is the FCA's accountability framework consisting of three components: "
                "(1) The Senior Managers Regime — requires pre-approval of individuals in senior positions "
                "(SMFs), with Statements of Responsibilities and a Duty of Responsibility requiring them to "
                "take reasonable steps. (2) The Certification Regime — firms must certify that relevant employees "
                "are 'fit and proper' annually. (3) Conduct Rules — basic standards applying to all staff. "
                "SMCR applies to all solo-regulated firms (banks, insurers, FCA-regulated firms) since "
                "December 2019 with three tiers: Enhanced, Core, and Limited Scope."
            ),
        },
        {
            "question": "What are the prescribed responsibilities under SMCR that must be allocated to senior managers?",
            "ground_truth": (
                "Prescribed responsibilities include: responsibility for the firm's performance of its "
                "obligations under the senior managers regime, compliance with CASS (client assets), "
                "money laundering reporting (MLRO function), compliance oversight, financial crime, "
                "whistleblowing, overseeing the firm's obligations under SYSC, responsibility for policies "
                "and procedures to counter financial crime, and ensuring adequacy of training for Conduct "
                "Rules staff. Enhanced firms must allocate additional prescribed responsibilities including "
                "responsibility for the firm's risk management and internal audit."
            ),
        },
        {
            "question": "How does the SMCR Duty of Responsibility differ from the previous Approved Persons Regime?",
            "ground_truth": (
                "Under the Approved Persons Regime, the FCA had to prove an individual was 'knowingly concerned' "
                "in a breach. Under SMCR's Duty of Responsibility (s66B FSMA), the burden is reversed: if "
                "a firm breaches a regulatory requirement in an area the senior manager is responsible for, "
                "the FCA can take action against the individual unless they can demonstrate they took 'reasonable "
                "steps' to prevent the breach. This significantly raises personal accountability."
            ),
        },

        # ── Consumer Duty ─────────────────────────────────────────────────
        {
            "question": "What are the four outcomes of the FCA's Consumer Duty and when did it come into force?",
            "ground_truth": (
                "The FCA Consumer Duty (PS22/9, FG22/5) came into force on 31 July 2023 for new and "
                "existing open products, and 31 July 2024 for closed products. The four outcomes are: "
                "(1) Products and Services — products must be designed to meet the needs of identified "
                "target markets. (2) Price and Value — firms must ensure fair value with a reasonable "
                "relationship between price and benefits. (3) Consumer Understanding — communications must "
                "equip consumers to make effective decisions. (4) Consumer Support — customer service must be "
                "at least as accessible as sales. These sit under the overarching principle: 'A firm must "
                "act to deliver good outcomes for retail customers.'"
            ),
        },
        {
            "question": "How should firms conduct a 'fair value assessment' under the Consumer Duty?",
            "ground_truth": (
                "Under the Consumer Duty (PRIN 2A.4), firms must assess whether the price consumers pay "
                "for a product is reasonable relative to its benefits. The assessment should consider: "
                "total costs to consumers (including opportunity costs), nature and quality of the product, "
                "benefits consumers receive, costs to the firm (manufacturing, distribution), market rates, "
                "characteristics of the target market (including vulnerable customers), and whether certain "
                "groups receive worse value. Firms must maintain documented evidence and review periodically."
            ),
        },
        {
            "question": "What monitoring and governance obligations does the Consumer Duty impose on firm boards?",
            "ground_truth": (
                "Under the Consumer Duty, boards and governing bodies must: produce and review an annual "
                "Consumer Duty board report assessing whether the firm is delivering good outcomes, "
                "ensure the Duty is embedded in the firm's strategy, culture, and business objectives, "
                "monitor and assess outcomes data across the four outcomes, challenge management on "
                "customer outcomes evidence, make the appointed Champion of the Consumer Duty report to "
                "the board regularly, and take action where outcomes for customers are poor. The FCA expects "
                "boards to maintain appropriate MI (management information) to evidence compliance."
            ),
        },

        # ── AML / KYC ────────────────────────────────────────────────────
        {
            "question": "What are the key requirements of the Money Laundering Regulations 2017 (as amended) for UK firms?",
            "ground_truth": (
                "The Money Laundering, Terrorist Financing and Transfer of Funds Regulations 2017 (MLR 2017, "
                "amended 2019 and 2022) require firms to: conduct risk assessments (firm-wide and per-client), "
                "implement customer due diligence (CDD) including identification and verification, apply "
                "enhanced due diligence (EDD) for high-risk situations (PEPs, high-risk countries, complex "
                "transactions), maintain records for 5 years, appoint a nominated officer (MLRO), provide "
                "staff training, report suspicious activity via SARs to the NCA, and register with a "
                "supervisory authority. Firms must also screen against UK and international sanctions lists."
            ),
        },
        {
            "question": "What is the difference between simplified due diligence, standard CDD, and enhanced due diligence under UK AML rules?",
            "ground_truth": (
                "Simplified Due Diligence (SDD) applies to low-risk clients (e.g., UK-listed companies, "
                "public authorities) — firms may reduce the extent of CDD measures but must still monitor. "
                "Standard CDD requires identifying and verifying client identity, beneficial ownership "
                "(25% threshold), understanding the purpose and nature of the business relationship, and "
                "ongoing monitoring. Enhanced Due Diligence (EDD) applies to high-risk situations — PEPs, "
                "customers from high-risk jurisdictions (FATF list), complex/unusual transactions — requiring "
                "additional identity verification, source of funds/wealth, senior management approval, "
                "and enhanced ongoing monitoring."
            ),
        },
        {
            "question": "How should a MLRO handle a Suspicious Activity Report (SAR) under the Proceeds of Crime Act 2002?",
            "ground_truth": (
                "The MLRO (Money Laundering Reporting Officer) must evaluate internal disclosures and, "
                "if suspicion is formed, submit a SAR to the National Crime Agency (NCA) via the SAR Online "
                "system. Under POCA 2002, the MLRO must: not tip off the subject (tipping off is a criminal "
                "offence under s333A), seek appropriate consent from the NCA before proceeding with relevant "
                "transactions (a Defence Against Money Laundering or DAML request), wait for the NCA's "
                "7-working-day notice period (31-day moratorium if refused), maintain confidential records, "
                "and ensure the firm does not commit a principal money laundering offence under ss327-329 POCA."
            ),
        },
        {
            "question": "What are the requirements for ongoing monitoring and transaction monitoring in AML compliance?",
            "ground_truth": (
                "Under MLR 2017 Regulation 28(11), firms must conduct ongoing monitoring including: "
                "scrutinising transactions throughout the business relationship to ensure consistency with "
                "knowledge of the customer, their risk profile, and source of funds; updating CDD records "
                "when triggered by changes in customer circumstances, new transactions, or passage of time; "
                "using automated transaction monitoring systems to detect unusual patterns; escalating flagged "
                "transactions for manual review; maintaining audit trails of monitoring activities; and "
                "documenting rationale for decisions not to file SARs on flagged matters."
            ),
        },

        # ── Sanctions ─────────────────────────────────────────────────────
        {
            "question": "How do UK sanctions regulations interact with AML obligations and what are the key screening requirements?",
            "ground_truth": (
                "UK sanctions are imposed under the Sanctions and Anti-Money Laundering Act 2018 (SAMLA) "
                "and various statutory instruments. Firms must screen clients, transactions, and beneficial "
                "owners against the OFSI (Office of Financial Sanctions Implementation) consolidated list. "
                "Unlike AML which is risk-based, sanctions compliance is absolute — any match requires "
                "asset freezing and OFSI reporting. Firms must screen at onboarding, on an ongoing basis "
                "(when lists are updated), and for all transactions. Breaching financial sanctions is a "
                "strict liability criminal offence. Firms should maintain auditable screening records "
                "and have clear escalation procedures for potential matches."
            ),
        },
        {
            "question": "What are the penalties for breaching UK financial sanctions and how is strict liability applied?",
            "ground_truth": (
                "Under SAMLA and relevant statutory instruments, breaching financial sanctions is a criminal "
                "offence carrying up to 7 years imprisonment and/or unlimited fines. OFSI can also impose "
                "monetary penalties on a strict liability basis (no intent required) of up to £1 million "
                "or 50% of the estimated value of the funds/resources, whichever is greater. The strict "
                "liability standard means firms cannot rely on 'reasonable excuse' — they must have robust "
                "systems to prevent breaches. OFSI publishes enforcement actions and maintains a public "
                "register of monetary penalties."
            ),
        },

        # ── Market Abuse (MAR) ────────────────────────────────────────────
        {
            "question": "What constitutes insider dealing under the UK Market Abuse Regulation and what are the key defences?",
            "ground_truth": (
                "Under UK MAR (Article 8), insider dealing occurs when a person possesses inside information "
                "(precise, not public, price-sensitive) and uses it to acquire or dispose of financial "
                "instruments, to cancel or amend existing orders, or recommends/induces another to deal. "
                "Key defences include: legitimate behaviour (Article 9) — e.g., executing a prior obligation, "
                "market-making in fulfilment of obligations, or executing orders on behalf of third parties. "
                "Firms must maintain insider lists (Article 18), implement information barriers (Chinese walls), "
                "and report suspicious transactions (STORs) under Article 16."
            ),
        },
        {
            "question": "What are the requirements for Suspicious Transaction and Order Reports (STORs) under MAR?",
            "ground_truth": (
                "Under UK MAR Article 16, firms that arrange or execute transactions must have effective "
                "arrangements and procedures to detect and report suspicious orders and transactions. "
                "STORs must be submitted to the FCA without delay when there is reasonable suspicion of "
                "insider dealing or market manipulation. The report must include: description of the order/ "
                "transaction, reasons for suspicion, identification of persons involved, capacity in which "
                "the reporter acts, and relevant supporting data. Firms must maintain records for 5 years "
                "and not inform the subject (no tipping off)."
            ),
        },
        {
            "question": "How does UK MAR define and prohibit market manipulation?",
            "ground_truth": (
                "UK MAR Article 12 defines market manipulation as: (a) entering into transactions, placing "
                "orders, or any other behaviour that gives false or misleading signals about supply/demand/ "
                "price or secures an abnormal/artificial price level; (b) transactions or orders employing "
                "fictitious devices or deception; (c) disseminating information that gives false or misleading "
                "signals (including rumour spreading). Annex I provides indicators including wash trades, "
                "spoofing/layering, painting the tape, pump and dump, and benchmark manipulation. The FCA "
                "can prosecute criminally under the Financial Services Act 2012 or impose civil penalties."
            ),
        },

        # ── PRIIPs ────────────────────────────────────────────────────────
        {
            "question": "What are the PRIIPs KID requirements and what information must be disclosed?",
            "ground_truth": (
                "Under the UK PRIIPs Regulation, manufacturers of Packaged Retail and Insurance-based "
                "Investment Products must produce a Key Information Document (KID) before a product is "
                "made available to retail investors. The KID must include: product description, summary "
                "risk indicator (SRI, scale 1-7), recommended holding period, performance scenarios "
                "(favourable, moderate, unfavourable, stress), costs and charges in monetary and percentage "
                "terms (including entry/exit costs, ongoing costs, incidental costs), and information about "
                "the complaint-handling process. The KID must be maximum 3 A4 pages, written in plain language."
            ),
        },
        {
            "question": "How are performance scenarios calculated in the PRIIPs KID?",
            "ground_truth": (
                "PRIIPs KID performance scenarios must present potential returns under stress, unfavourable, "
                "moderate, and favourable conditions at the recommended holding period and intermediate "
                "periods. For Category 2 products (with sufficient historical data), scenarios are based on "
                "historical performance distributions using percentile methodology: stress (10th percentile "
                "stressed), unfavourable (25th percentile), moderate (50th percentile), and favourable "
                "(75th percentile). All scenarios must deduct costs and show net returns both in monetary "
                "terms and as a percentage annual return."
            ),
        },

        # ── GDPR in Financial Services ────────────────────────────────────
        {
            "question": "How does GDPR apply to financial firms processing customer data in the UK, and what is the role of the ICO?",
            "ground_truth": (
                "UK GDPR (retained EU GDPR post-Brexit, supplemented by the Data Protection Act 2018) "
                "requires financial firms to: identify lawful bases for processing (legitimate interest, "
                "contract performance, legal obligation are most common), implement data protection by "
                "design and default, appoint a DPO where required, maintain Records of Processing Activities, "
                "conduct DPIAs for high-risk processing, report breaches to the ICO within 72 hours, and "
                "honour data subject rights (access, rectification, erasure, portability). The ICO "
                "(Information Commissioner's Office) supervises compliance and can issue fines up to "
                "£17.5 million or 4% of global turnover."
            ),
        },
        {
            "question": "What are the lawful bases for processing personal data under UK GDPR and which apply most in finance?",
            "ground_truth": (
                "UK GDPR Article 6 provides six lawful bases: (1) Consent, (2) Contractual necessity, "
                "(3) Legal obligation, (4) Vital interests, (5) Public task, (6) Legitimate interests. "
                "In financial services, the most commonly relied upon are: Legal Obligation (AML/CDD, "
                "regulatory reporting, sanctions screening), Contractual Necessity (processing transactions, "
                "account management), and Legitimate Interests (fraud prevention, internal analytics) subject "
                "to a balancing test. Consent is generally avoided for core financial processing as it can "
                "be withdrawn, but may be used for marketing communications."
            ),
        },

        # ── Whistleblowing ────────────────────────────────────────────────
        {
            "question": "What are the FCA's requirements for whistleblowing arrangements under SYSC 18?",
            "ground_truth": (
                "Under SYSC 18, firms with more than 250 UK employees (and all relevant authorised persons) "
                "must: appoint a senior manager as 'whistleblowers' champion' responsible for oversight, "
                "establish internal whistleblowing channels, put in place procedures for handling disclosures, "
                "include whistleblowing in induction training and regular refreshers, inform employees about "
                "the FCA whistleblowing service, include a term in settlement agreements that workers can "
                "still make protected disclosures to the FCA/PRA, and present annually to the board on "
                "whistleblowing. The FCA also operates its own whistleblowing hotline for direct reports."
            ),
        },
        {
            "question": "How does the Public Interest Disclosure Act 1998 protect whistleblowers in financial services?",
            "ground_truth": (
                "PIDA 1998 (as amended by the Enterprise and Regulatory Reform Act 2013) protects workers "
                "who make 'qualifying disclosures' about: criminal offences, failure to comply with legal "
                "obligations, miscarriages of justice, health and safety dangers, environmental damage, "
                "or deliberate concealment of any of these. Financial sector workers can disclose to the "
                "FCA as a 'prescribed person.' Protection includes immunity from dismissal or detriment, "
                "and any 'gagging clauses' in contracts are void to the extent they prevent protected "
                "disclosures to regulators."
            ),
        },

        # ── Capital Adequacy ──────────────────────────────────────────────
        {
            "question": "What are the key prudential capital requirements for MIFIDPRU investment firms in the UK?",
            "ground_truth": (
                "MIFIDPRU (effective 1 January 2022) replaced the EU CRD IV/CRR framework for FCA-regulated "
                "investment firms. Key requirements include: permanent minimum capital (PMR) of £75,000, "
                "£150,000, or £750,000 depending on firm type; fixed overheads requirement (FOR) — 25% of "
                "annual fixed overheads; K-factor requirement based on risks to clients (K-AUM, K-COH, "
                "K-ASA, K-CMH), market (K-NPR, K-CMG), and firm (K-DTF, K-CON, K-TCD). The own funds "
                "requirement is the higher of PMR, FOR, and K-factor total. Firms must maintain Common "
                "Equity Tier 1 of at least 56% of their requirement."
            ),
        },
        {
            "question": "What is the ICARA process and how does it differ from the ICAAP?",
            "ground_truth": (
                "The Internal Capital Adequacy and Risk Assessment (ICARA) under MIFIDPRU replaces the "
                "previous ICAAP (Internal Capital Adequacy Assessment Process) for investment firms. "
                "Key differences: ICARA is forward-looking and covers both capital and liquidity (ICAAP was "
                "capital-only); ICARA uses the 'harm' framework assessing risks of harm to clients, markets, "
                "and the firm itself; ICARA must assess wind-down planning and trigger points; it must be "
                "reviewed at least annually and whenever material changes occur. The ICARA should drive "
                "business decisions and be approved by the governing body."
            ),
        },

        # ── Operational Resilience ────────────────────────────────────────
        {
            "question": "What does the FCA's operational resilience framework (PS21/3) require from firms?",
            "ground_truth": (
                "PS21/3 (effective 31 March 2022, full compliance by 31 March 2025) requires firms to: "
                "identify their Important Business Services (IBS), set impact tolerances for maximum "
                "tolerable disruption, map resources and dependencies supporting each IBS (people, processes, "
                "technology, facilities, information), conduct scenario testing within impact tolerances, "
                "develop and maintain self-assessment documents, maintain communication plans for disruptions, "
                "ensure third-party dependencies are captured, and review annually. The aim is that firms "
                "can prevent, adapt, respond to, recover, and learn from operational disruptions."
            ),
        },
        {
            "question": "How should firms define and test their impact tolerances under the operational resilience framework?",
            "ground_truth": (
                "Firms must set impact tolerances for each Important Business Service, expressed as a "
                "maximum tolerable level of disruption (typically measured in time but can include other "
                "metrics like data loss). Testing should include: severe but plausible scenarios, assumption "
                "that disruption has occurred (not just prevention), involvement of key stakeholders, "
                "testing of people/processes/technology/third parties, tabletop exercises and live "
                "simulations, documenting lessons learned and remediation plans. Firms must be able to "
                "remain within impact tolerances by March 2025."
            ),
        },

        # ── Cross-cutting Compliance ──────────────────────────────────────
        {
            "question": "What is the relationship between the Senior Managers Regime and the Consumer Duty?",
            "ground_truth": (
                "The SMCR and Consumer Duty are complementary: the Consumer Duty sets the standard of "
                "outcomes firms must deliver, while SMCR ensures individual accountability for achieving "
                "those outcomes. The FCA expects firms to allocate Consumer Duty responsibilities to specific "
                "Senior Managers (typically the CEO or designated executive) via Statements of Responsibilities. "
                "Under SMCR's Duty of Responsibility, senior managers can face personal regulatory action "
                "if they fail to take reasonable steps to ensure Consumer Duty compliance in their areas. "
                "The Conduct Rules also require all staff to act in a way consistent with delivering "
                "good customer outcomes."
            ),
        },
        {
            "question": "How do firms reconcile GDPR data minimisation with AML record-keeping requirements?",
            "ground_truth": (
                "Firms face tension between GDPR's data minimisation principle (collect only what's necessary) "
                "and MLR 2017's requirement to retain CDD records for 5 years after the relationship ends. "
                "The reconciliation is that AML processing falls under the GDPR 'legal obligation' lawful "
                "basis and the 'archiving in the public interest' exemption. Firms should: clearly define "
                "retention schedules aligned with legal requirements, document the legal basis for each "
                "category of data, delete data promptly after the retention period expires, and maintain "
                "a data retention policy that maps regulatory requirements to specific data types."
            ),
        },
        {
            "question": "What are the FCA's expectations for climate-related financial disclosures by regulated firms?",
            "ground_truth": (
                "The FCA requires TCFD-aligned (Task Force on Climate-related Financial Disclosures) "
                "reporting for premium-listed companies and asset managers with AUM above £50bn (reducing "
                "to £5bn from 2023). PS21/24 requires disclosures across the four TCFD pillars: Governance "
                "(board oversight of climate risks), Strategy (actual/potential impacts and scenario analysis), "
                "Risk Management (processes for identifying/assessing climate risks), and Metrics/Targets "
                "(GHG emissions, climate-related performance metrics). SDR (Sustainability Disclosure "
                "Requirements) introduced in 2023 further extends these obligations and introduces "
                "anti-greenwashing rules for all FCA-regulated firms."
            ),
        },
        {
            "question": "What are the regulatory requirements for outsourcing critical functions in UK financial services?",
            "ground_truth": (
                "Under SYSC 8 (and MIFIDPRU for investment firms), firms outsourcing critical or important "
                "functions must: conduct thorough due diligence on service providers, have a legally binding "
                "written agreement covering service levels, data protection, audit rights, business continuity, "
                "sub-outsourcing restrictions, and termination provisions. The firm's board retains ultimate "
                "responsibility and must not outsource in a way that impairs quality of governance. "
                "An outsourcing register must be maintained. The FCA and PRA must be notified before "
                "outsourcing critical banking functions. The firm must maintain the ability to transfer "
                "to an alternative provider or bring services in-house."
            ),
        },
        {
            "question": "How do the FCA's financial promotions rules apply to digital marketing and social media?",
            "ground_truth": (
                "Under COBS 4 and the Financial Promotions Order (FPO), all financial promotions must be "
                "fair, clear, and not misleading. For digital and social media: promotions must comply "
                "regardless of the medium (including tweets, posts, influencer content); risk warnings "
                "must be prominent and not obscured; firms are responsible for promotions made by appointed "
                "representatives and affiliates; 'real-time' promotions on social media are subject to rules "
                "on unsolicited contact. From 2023, the FCA Gateway requires unauthorised firms to obtain "
                "FCA approval for crypto-asset promotions. Firms must archive all digital promotions and "
                "maintain approval records."
            ),
        },

        # ── Advanced & Emerging Topics ────────────────────────────────────
        {
            "question": "What are the requirements for cryptoasset firms under the FCA's financial promotions regime?",
            "ground_truth": (
                "From 8 October 2023, PS23/6 extended financial promotions rules to qualifying cryptoassets. "
                "Key requirements: promotions must be fair, clear, and not misleading; must include a "
                "prominent risk warning ('Don't invest unless you're prepared to lose all the money you "
                "invest'); a 24-hour cooling-off period for first-time investors; prohibition on "
                "incentives-to-invest (e.g., refer-a-friend bonuses); client appropriateness assessments; "
                "and clear explanations of risks. Unauthorised firms must have promotions approved by an "
                "FCA-authorised firm. The FCA maintains a warning list and has taken enforcement action "
                "against non-compliant promotions."
            ),
        },
        {
            "question": "How does the FCA approach regulation of AI and machine learning in financial services?",
            "ground_truth": (
                "The FCA takes a principles-based approach to AI/ML under existing rules rather than "
                "specific AI legislation. Key expectations include: firms must be able to explain AI-driven "
                "decisions to consumers and regulators (explainability), ensure AI models do not unfairly "
                "discriminate (fairness), validate and monitor model performance on an ongoing basis, "
                "maintain human oversight and accountability under SMCR, conduct robust testing including "
                "bias testing, and ensure data quality and governance. The FCA-BOE AI Public-Private Forum "
                "published discussion papers in 2022-23 providing guidance. Firms using AI for consumer "
                "outcomes must demonstrate compliance with the Consumer Duty."
            ),
        },
        {
            "question": "What is the FCA's approach to Open Banking and Open Finance regulation?",
            "ground_truth": (
                "Open Banking in the UK was mandated by the CMA's Retail Banking Market Investigation Order "
                "2017, requiring the CMA9 banks to provide regulated APIs. The FCA regulates Account "
                "Information Service Providers (AISPs) and Payment Initiation Service Providers (PISPs) "
                "under PSR 2017. Requirements include: FCA authorisation/registration, strong customer "
                "authentication (SCA), explicit customer consent for data access, data minimisation (only "
                "access data necessary for the service), and consumer protection. The FCA is extending "
                "this framework to 'Open Finance' covering savings, insurance, and pensions data with "
                "similar principles of customer consent and data security."
            ),
        },
        {
            "question": "What are the requirements for business continuity planning under FCA regulation?",
            "ground_truth": (
                "Under SYSC 4.1.6R, firms must have sound administrative and accounting procedures, "
                "internal control mechanisms, and effective risk assessment. Business continuity planning "
                "requirements include: conducting business impact analysis to identify critical functions, "
                "developing documented BCP and disaster recovery plans, testing plans at least annually, "
                "establishing a crisis management team and communication protocols, ensuring IT systems "
                "resilience and data backup, considering pandemic and remote working scenarios, maintaining "
                "alternative premises and recovery sites where appropriate, and integrating BCP with the "
                "broader operational resilience framework under PS21/3."
            ),
        },
        {
            "question": "How does the UK regulate payment services and what are the key requirements under PSR 2017?",
            "ground_truth": (
                "The Payment Services Regulations 2017 (PSR 2017) implement PSD2 in the UK. Key requirements: "
                "firms providing payment services must be authorised/registered by the FCA; must safeguard "
                "client funds (segregation or insurance); must implement Strong Customer Authentication (SCA) "
                "for electronic payments using two of three factors (knowledge, possession, inherence); "
                "must provide transparent pricing and execution times; handle complaints within 15 business "
                "days (35 in exceptional cases); maintain minimum capital requirements (€20,000 to €125,000 "
                "depending on services); implement fraud prevention measures; and report significant "
                "operational/security incidents to the FCA."
            ),
        },
        {
            "question": "What are the regulatory requirements for firms offering contracts for difference (CFDs) to retail clients in the UK?",
            "ground_truth": (
                "The FCA imposed permanent measures on CFDs for retail clients (PS19/18): leverage limits "
                "(30:1 for major FX, 20:1 for non-major FX/gold/major indices, 10:1 for other commodities, "
                "5:1 for individual equities, 2:1 for cryptocurrencies); standardised margin close-out "
                "at 50% of minimum required margin; negative balance protection per account; prohibition on "
                "monetary and non-monetary incentives; mandatory risk warning stating percentage of retail "
                "accounts that lose money; and a ban on the sale, marketing, and distribution of binary "
                "options to retail consumers."
            ),
        },
        {
            "question": "What is the FCA's approach to vulnerable customers and what are firms' obligations?",
            "ground_truth": (
                "FG21/1 (Guidance for firms on the fair treatment of vulnerable customers) defines a "
                "vulnerable customer as someone who, due to personal circumstances, is especially susceptible "
                "to harm. Firms must: understand the nature and scale of vulnerability in their target market, "
                "train staff to recognise and respond to vulnerability, design products and services to meet "
                "needs of vulnerable customers, provide flexible communication approaches, monitor outcomes "
                "for vulnerable vs. non-vulnerable customers, and create a supportive environment where "
                "customers can disclose circumstances. Under the Consumer Duty, firms must pay particular "
                "attention to outcomes for vulnerable customers across all four outcome areas."
            ),
        },
        {
            "question": "How do the FCA's Listing Rules and Prospectus Regulation interact for companies seeking to list on UK markets?",
            "ground_truth": (
                "The FCA's Listing Rules (LR) set requirements for companies admitted to the Official List, "
                "including eligibility criteria, continuing obligations, and corporate governance standards. "
                "The UK Prospectus Regulation (retained EU legislation) requires a prospectus when securities "
                "are offered to the public or admitted to trading on a regulated market, unless an exemption "
                "applies. Key interactions: the prospectus must comply with content requirements (risk factors, "
                "financial information, business description), undergo FCA review and approval, and be made "
                "publicly available. The Listing Rules then impose continuing obligations including timely "
                "disclosure of inside information (DTR 2), annual financial reporting, and related party "
                "transaction rules."
            ),
        },
    ]
