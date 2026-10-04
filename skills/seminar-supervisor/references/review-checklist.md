# Seminar Supervisor Review Checklist

Use this catalog as a set of tests, not as a quota. Apply all universal sections and every relevant conditional lens. Report a rule only when the artifact supplies evidence of a defect, probable risk, consequential omission, or blocking uncertainty.

## Contents

1. Review calibration
2. Purpose, scope, and contract
3. Concepts, definitions, and notation
4. Reference, identity, and abstraction
5. Consistency and logical form
6. Argument and inference
7. Evidence, sources, and citations
8. Quantitative and statistical claims
9. Causality, comparison, and uncertainty
10. Completeness, boundaries, and edge cases
11. Time, state, process, and data flow
12. Decisions, alternatives, tradeoffs, and risk
13. Feasibility, adoption, and operations
14. Structure and communication
15. Examples, visuals, tables, and code excerpts
16. Integrity, safety, security, privacy, and accessibility
17. Academic and research lens
18. Technical architecture and design lens
19. Plans, specifications, and requirements lens
20. Code explanation and API documentation lens
21. Presentation and seminar lens
22. Procedures and instructional material lens
23. Data analysis and results lens
24. Policy, strategy, and business case lens
25. False-positive controls
26. Final acceptance audit

## 1. Review Calibration

- Identify whether the artifact is exploratory, proposed, authoritative, executable, evidentiary, or final.
- Apply stricter completeness standards to artifacts that authorize action or claim finality.
- Calibrate definitions to the stated audience without excusing local jargon or contested terms.
- Separate defects visible in the artifact from facts that require external verification.
- Separate semantic correctness from rhetorical effectiveness and production polish.
- Separate a missing decision from a deliberate extension point.
- Require every extension point to state the invariant it preserves and the decision it defers.
- Trace each criticism to an observable passage, omission, dependency, or requirement.
- Prefer root-cause findings over lists of symptoms.
- Treat repeated local symptoms as evidence of a systemic defect when appropriate.
- Verify that each proposed repair addresses the cited consequence.
- Reassess severity after accounting for nearby qualifications and definitions.
- Note the reviewed scope, evidence base, and any inaccessible material.
- Avoid claiming exhaustiveness when source access or domain verification is incomplete.

## 2. Purpose, Scope, and Contract

- Require a discernible governing question, objective, decision, or deliverable.
- Check that the title, abstract, opening, body, and conclusion describe the same undertaking.
- Check that the artifact answers the requested question rather than a nearby easier question.
- Check that declared goals are outcomes rather than vague activities.
- Check that success criteria are observable and aligned with the goal.
- Check that evaluation criteria appear before conclusions that depend on them.
- Check that the intended audience and their assumed knowledge are coherent.
- Check that audience needs determine detail, terminology, and examples.
- Check that mandatory requirements are distinguished from preferences.
- Check that explicit constraints are preserved throughout the proposal.
- Check that implicit constraints are surfaced when they materially affect feasibility.
- Check that inclusions and exclusions are explicit enough to prevent incompatible readings.
- Check that excluded work does not contain a prerequisite for included work.
- Check that a scope boundary does not silently weaken a broad claim.
- Check that geographic, temporal, population, platform, organizational, and domain boundaries are stated when relevant.
- Check that the unit of analysis remains stable.
- Check that deliverables, decisions, and non-goals are not conflated.
- Check that stakeholder expectations are identified when acceptance depends on them.
- Check that authoritative sources and precedence rules are named when requirements conflict.
- Check that completion, acceptance, and approval are not treated as synonyms without justification.
- Check that the artifact does not promise outcomes beyond its authority or available evidence.
- Check that future extension is reserved where a present choice would otherwise create avoidable lock-in.
- Reject decorative statements of purpose that do not constrain content or decisions.

## 3. Concepts, Definitions, and Notation

- Identify every concept that is specialized, overloaded, locally redefined, contested, measured, or central to the conclusion.
- Require each such concept to be defined before its first consequential use.
- Reject definitions that merely restate the term with synonyms.
- Reject circular definitions in which each term depends on the other.
- Reject definitions that rely on a later undefined concept.
- Check that definitions state inclusion and exclusion boundaries where ambiguity matters.
- Check that operational definitions match how observations or measurements are produced.
- Check that normative terms such as good, fair, efficient, robust, scalable, simple, or successful have criteria.
- Check that comparative terms identify the comparison class and baseline.
- Check that relative terms such as recent, large, fast, common, or significant have context.
- Check that modal terms such as must, should, may, can, and will are used deliberately.
- Check that universal and existential quantifiers are explicit when inference depends on them.
- Check that names, abbreviations, symbols, and acronyms are introduced before use.
- Check that identical symbols do not denote different entities in the same scope.
- Check that different symbols do not denote the same entity without explanation.
- Check that singular and plural forms do not change conceptual scope.
- Check that capitalization and typography do not imply inconsistent semantic distinctions.
- Check that the same term retains the same meaning across sections.
- Check that a changed definition is announced and justified.
- Check that an example is not substituted for a definition.
- Check that implementation details are not smuggled into a domain definition.
- Check that a label does not presuppose the disputed conclusion.
- Check that categories are mutually exclusive when the argument treats them as such.
- Check that categories are collectively exhaustive when the argument assumes full coverage.
- Check that taxonomies state the dimension along which items are classified.
- Check that levels, stages, priorities, and severities have ordering rules.
- Check that aliases and historical names cannot create mistaken identity.
- Check that glossary definitions agree with body usage.
- Flag use-before-definition even when a definition eventually appears.
- Prefer moving the definition to first use over forcing readers to search backward or forward.

## 4. Reference, Identity, and Abstraction

- Check every pronoun, demonstrative, cross-reference, and shorthand for a unique antecedent.
- Check that terms such as this, that, it, they, former, latter, above, and below remain unambiguous after editing or reordering.
- Check that entities with similar names remain distinguishable.
- Check that versions, variants, environments, populations, and time periods are not conflated.
- Check that an object, representation, identifier, and observation of that object are not treated as identical.
- Check that a model is not confused with the modeled system.
- Check that a proxy is not confused with the target construct.
- Check that a type is not confused with an instance.
- Check that a class is not confused with a member.
- Check that a process is not confused with its outcome.
- Check that a capability is not confused with evidence that it was exercised.
- Check that an interface promise is not confused with one implementation.
- Check that descriptive and normative claims remain distinct.
- Check that logical, conceptual, implementation, deployment, and user-interface levels are not mixed without a bridge.
- Check that local behavior is not generalized to system behavior without composition evidence.
- Check that aggregate behavior is not attributed to each member without justification.
- Check that a change in granularity does not invalidate comparison or inference.
- Check that the artifact states when it intentionally changes abstraction level.
- Require stable identifiers for referenced requirements, decisions, figures, interfaces, and findings when the artifact is long or maintained over time.

## 5. Consistency and Logical Form

- Compare every conclusion with the premises and definitions it depends on.
- Search for direct contradictions between affirmative and negative claims.
- Search for incompatible numeric values, dates, names, statuses, priorities, and requirements.
- Search for promises in summaries that are narrowed or abandoned in the body.
- Search for caveats in the body that are omitted from conclusions.
- Search for mutually exclusive assumptions used in different sections.
- Check that examples obey the stated rules.
- Check that tables, figures, captions, appendices, and body text agree.
- Check that normative requirements do not conflict with described behavior.
- Check that dependency direction is acyclic unless iteration is explicit.
- Check that prerequisites occur before dependent actions.
- Check that a fallback does not depend on the failed mechanism.
- Check that an exception does not swallow the rule.
- Check that a special case does not contradict a claimed invariant.
- Check that priority and precedence rules resolve simultaneous conditions.
- Check that terms such as always, never, only, exactly, all, and none survive counterexamples.
- Check that necessary conditions are not presented as sufficient.
- Check that sufficient conditions are not presented as necessary.
- Check that possibility is not presented as probability or certainty.
- Check that absence of evidence is not presented as evidence of absence without a detection argument.
- Check that an inability to reject is not presented as proof.
- Check that mutually compatible explanations are not framed as exclusive alternatives.
- Check that the conclusion does not exceed the strongest supported premise.
- Distinguish contradiction from a valid tradeoff, scoped exception, temporal change, or refinement.
- Require explicit reconciliation when two authoritative sources disagree.

## 6. Argument and Inference

- Identify the central conclusion and each supporting premise.
- Require every central claim to have a traceable support path.
- Flag orphan claims that support the conclusion but lack evidence or argument.
- Flag irrelevant evidence that does not bear on the stated claim.
- Flag circular support in which the conclusion is assumed by a premise.
- Flag question-begging definitions that encode the desired outcome.
- Flag non sequiturs where the conclusion does not follow from the preceding material.
- Flag hidden premises required to make the inference valid.
- Flag equivocation when a term changes meaning across an inference.
- Flag category errors between facts, values, capabilities, processes, and outcomes.
- Flag composition and division errors.
- Flag false dilemmas that omit live alternatives.
- Flag straw-man representations of alternatives or objections.
- Flag appeals to authority when authority is irrelevant, unqualified, or substituted for evidence.
- Flag appeals to popularity, tradition, novelty, nature, or consequences when they do not establish truth.
- Flag anecdotal support for population-level claims.
- Flag cherry-picked examples, time windows, metrics, or sources.
- Flag moving goalposts and post hoc criteria changes.
- Flag self-sealing claims that cannot be contradicted by any observation.
- Flag unfalsifiable claims presented as empirical conclusions.
- Flag tautologies presented as discoveries.
- Flag rhetorical questions that carry an unsupported premise.
- Flag loaded language that biases classification or hides alternatives.
- Flag conclusions based only on an example when a general proof is required.
- Flag inductive claims that omit sampling and representativeness limits.
- Flag deductive claims with invalid form even when the conclusion happens to be true.
- Require objections to be answered at their strongest plausible form.
- Construct a counterexample against each universal or exclusivity claim.
- Check whether the argument survives reversing a favored assumption.
- Check whether the conclusion would change under a plausible alternate interpretation.
- Distinguish demonstrated fact, interpretation, hypothesis, recommendation, and speculation.

## 7. Evidence, Sources, and Citations

- Require evidence proportional to the importance and specificity of the claim.
- Check that each citation supports the exact proposition attributed to it.
- Check primary sources when secondary summaries could distort the claim.
- Check source authority, competence, independence, and conflicts of interest.
- Check publication date and whether the evidence remains current for the claim.
- Check jurisdiction, population, environment, version, and context match.
- Check whether cited results are observational, experimental, simulated, anecdotal, or opinion.
- Check whether the artifact distinguishes source findings from its own interpretation.
- Check whether quotations preserve qualifying context.
- Check whether paraphrases preserve modality and uncertainty.
- Check whether citations are attached to the relevant claim rather than a distant paragraph.
- Check whether every borrowed definition, number, method, and non-obvious factual claim has appropriate provenance.
- Check whether a source is cited repeatedly as independent evidence when all citations share one origin.
- Check whether sources represent genuine corroboration rather than citation copying.
- Check whether negative or conflicting evidence is acknowledged.
- Check whether evidence selection rules were established before observing results.
- Check whether missing data and inaccessible sources are disclosed.
- Check whether unpublished, non-peer-reviewed, or vendor evidence is labeled appropriately.
- Check whether links, identifiers, titles, authors, and dates permit source recovery.
- Check whether a citation exists and is not fabricated.
- Do not infer that an uncited claim is false; classify it as unsupported until verified.
- Do not claim source verification unless the source was actually inspected.
- Request the minimum additional evidence that could resolve the finding.

## 8. Quantitative and Statistical Claims

- Check units, dimensions, scales, denominators, and time windows.
- Check that quantities being compared use compatible units and definitions.
- Check arithmetic, totals, percentages, rates, ratios, and percentage-point differences.
- Check whether percentages identify their denominator.
- Check whether averages specify mean, median, mode, or another summary.
- Check whether averages hide distribution, variance, skew, or subgroups relevant to the conclusion.
- Check whether counts are independent or duplicated.
- Check whether samples represent the target population.
- Check sampling frame, inclusion criteria, exclusion criteria, attrition, and missingness.
- Check whether sample size supports the claimed precision.
- Check whether uncertainty intervals accompany estimates when needed.
- Check whether confidence intervals are interpreted correctly.
- Check whether statistical significance is distinguished from practical importance.
- Check whether effect size is reported and contextualized.
- Check whether multiple comparisons, repeated looks, or researcher degrees of freedom are addressed.
- Check whether model assumptions are stated and tested.
- Check whether training, validation, and test data remain separated.
- Check whether hyperparameter selection leaked test information.
- Check whether metrics align with the real objective and failure costs.
- Check whether a metric can be gamed or improved while the real outcome worsens.
- Check baseline selection and whether the baseline is competitive and comparable.
- Check whether relative improvement hides a small absolute effect.
- Check whether absolute totals hide exposure or population growth.
- Check whether missing values, censoring, truncation, and outliers are handled transparently.
- Check whether aggregation creates Simpson's paradox or masks subgroup reversal.
- Check whether visual axes, bins, normalization, smoothing, and truncation distort perception.
- Check whether forecasts state horizon, assumptions, intervals, and validation method.
- Check whether sensitivity analysis covers outcome-critical parameters.
- Check whether numerical precision exceeds measurement or model precision.
- Recompute decisive quantities when data are available; otherwise state that arithmetic was not independently verified.

## 9. Causality, Comparison, and Uncertainty

- Distinguish correlation, prediction, association, contribution, mechanism, and causation.
- Require temporal precedence for causal claims.
- Identify plausible confounders, mediators, colliders, and selection effects.
- Check whether conditioning choices introduce bias.
- Check whether intervention and control groups are comparable.
- Check randomization, blinding, contamination, compliance, and spillovers when applicable.
- Check whether before-and-after comparisons account for secular trends.
- Check whether attribution distinguishes the proposed change from concurrent changes.
- Check whether mechanisms are evidenced rather than merely narrated.
- Check whether reverse causality remains plausible.
- Check whether a proxy outcome supports the claimed real-world outcome.
- Check whether counterfactual claims identify a defensible comparison.
- Check whether alternatives use the same evaluation criteria, scope, and evidence standard.
- Check whether costs and benefits are counted symmetrically across alternatives.
- Check whether the favored option receives unearned assumptions denied to alternatives.
- Check whether uncertainty sources are named: measurement, sampling, model, scenario, implementation, and unknown unknowns where relevant.
- Check whether confidence language matches evidence strength.
- Check whether ranges and scenarios have justified bounds.
- Check whether best-case, expected, and worst-case cases use internally consistent assumptions.
- Check whether uncertainty is propagated through dependent calculations or decisions.
- Check whether a recommendation remains robust under plausible uncertainty.

## 10. Completeness, Boundaries, and Edge Cases

- Enumerate inputs, outputs, actors, states, dependencies, and external systems implied by the artifact.
- Check normal, empty, minimum, maximum, boundary, malformed, duplicate, delayed, partial, and adversarial cases.
- Check initial, steady, degraded, recovery, migration, and terminal states.
- Check first-use, repeated-use, concurrent-use, interrupted-use, and abandoned-use behavior.
- Check optional and missing values.
- Check zero, negative, overflow, underflow, precision, and unit edge cases when numerical behavior matters.
- Check internationalization, localization, time zone, calendar, encoding, and text-direction concerns when relevant.
- Check identity collision, stale reference, deletion, rename, and version skew.
- Check partial success and whether retries duplicate effects.
- Check timeout, cancellation, reordering, late arrival, and loss.
- Check inconsistent external state and unavailable dependencies.
- Check permission denial and role changes during an operation.
- Check how invalid assumptions are detected and surfaced.
- Check whether exceptions have defined handling rather than silent omission.
- Check whether default behavior is explicit and safe.
- Check precedence when multiple rules apply.
- Check whether every branch reaches a coherent outcome.
- Check whether all promised outputs have a producing step.
- Check whether all inputs have validation and ownership.
- Check whether all requirements map to behavior and verification.
- Check whether known limitations have consequences and containment measures.
- Check whether out-of-scope cases are rejected, deferred, or safely degraded.
- Check whether future extension points preserve identifiers, invariants, compatibility, and ownership boundaries.
- Do not demand speculative machinery for remote cases; require a deliberate boundary and extensible design instead.

## 11. Time, State, Process, and Data Flow

- Identify the source of truth for each mutable fact.
- Identify state ownership and legal state transitions.
- Check that transitions define preconditions, triggers, effects, and postconditions.
- Check that impossible states are excluded or detected.
- Check that repeated transitions are idempotent when retries are possible.
- Check ordering guarantees and behavior under reordering.
- Check synchronization and consistency expectations across replicas or components.
- Check transaction boundaries and partial-commit behavior.
- Check rollback or compensation for multi-step failure.
- Check lifecycle behavior for creation, activation, suspension, expiration, deletion, and restoration.
- Check whether time is event time, processing time, wall time, monotonic time, or a business date.
- Check clock skew, daylight-saving changes, leap behavior, time zones, and ambiguous local times when relevant.
- Check retention, expiration, archival, and deletion timing.
- Check whether historical interpretation changes after definitions or schemas evolve.
- Check data lineage from origin through transformation to output.
- Check transformations for loss, coercion, normalization, deduplication, and ordering.
- Check whether every consumer sees data in the promised shape and freshness.
- Check whether feedback loops can amplify errors or create instability.
- Check whether caches have invalidation and staleness semantics.
- Check whether asynchronous work exposes intermediate states.
- Check whether recovery replays events safely.
- Check whether audit history remains attributable and tamper-evident when required.

## 12. Decisions, Alternatives, Tradeoffs, and Risk

- Require the decision to be stated separately from its rationale.
- Require decision criteria before comparing alternatives.
- Check that all credible alternatives, including doing nothing, are considered when material.
- Check that rejected alternatives receive a fair description.
- Check that alternatives are compared at the same maturity and scope.
- Check that tradeoffs include both benefits and costs.
- Check short-term and long-term consequences.
- Check reversible and irreversible aspects of the decision.
- Check lock-in, switching cost, path dependence, and exit options.
- Check opportunity cost and displaced work.
- Check operational, organizational, legal, security, financial, reputational, and ethical risk as applicable.
- Check probability and impact separately.
- Check risk owners, triggers, mitigations, contingencies, and residual exposure.
- Check whether mitigation introduces a new risk.
- Check whether risk acceptance has an authorized owner.
- Check whether assumptions behind the decision have review dates or invalidation signals.
- Check whether a pilot can test decisive uncertainty without prejudging full adoption.
- Check whether decision deadlines are genuine constraints or arbitrary pressure.
- Check whether sunk costs improperly influence the recommendation.
- Check whether a local optimum harms the wider system.
- Check whether incentives align with the desired outcome.
- Check whether success for one stakeholder transfers cost to another without acknowledgment.
- Require explicit rationale for omitting a plausible future extension that would be expensive to retrofit.

## 13. Feasibility, Adoption, and Operations

- Check that required capabilities, resources, authority, budget, time, and expertise exist or are planned.
- Check that dependencies have owners and credible availability.
- Check sequencing, critical path, and prerequisite completion.
- Check that ownership persists after initial delivery.
- Check who operates, supports, updates, and retires the result.
- Check compatibility with existing processes, systems, policies, and user expectations.
- Check migration of data, behavior, users, integrations, and documentation.
- Check coexistence during transition and version skew.
- Check backward and forward compatibility where relevant.
- Check rollout stages, gates, monitoring, abort criteria, and recovery.
- Check whether rollback is technically and operationally possible after state changes.
- Check training, communication, discoverability, and support needs.
- Check adoption incentives and sources of resistance.
- Check accessibility and accommodation needs before rollout.
- Check capacity, throughput, latency, storage, cost, and growth assumptions.
- Check reliability targets and degraded-mode behavior.
- Check observability for success, failure, performance, and misuse.
- Check alert ownership, diagnostic context, and response procedures.
- Check maintenance burden, dependency lifecycle, and upgrade strategy.
- Check deprecation, replacement, data export, and end-of-life behavior.
- Check testing at unit, integration, system, compatibility, performance, security, recovery, and acceptance levels as applicable.
- Check whether acceptance criteria can be evaluated by an independent party.
- Check whether documentation and runbooks reflect actual behavior.
- Check whether extension mechanisms have stable contracts rather than speculative placeholders.

## 14. Structure and Communication

- Put the governing question, thesis, decision, or requested action where the audience can find it promptly.
- Check that section order follows conceptual and dependency order.
- Define terms before dependent discussion.
- Present evidence before conclusions that require it, unless a summary is explicitly labeled.
- Check that headings accurately predict their content.
- Check that parallel sections use comparable structure.
- Check that transitions explain why the next section follows.
- Check that paragraphs have one controlling purpose.
- Check that topic sentences and conclusions match paragraph evidence.
- Remove repetition that does not add a new implication, qualification, or perspective.
- Preserve repetition needed for summaries, navigation, or high-risk instructions.
- Check that summaries retain decisive caveats.
- Check that detail is placed where readers need it rather than in an unrelated appendix.
- Check that cross-references are stable and accurate.
- Check that the conclusion synthesizes rather than merely repeats.
- Check that recommendations identify actor, action, object, timing, and condition.
- Replace vague verbs such as handle, support, optimize, improve, address, and ensure with observable behavior where precision matters.
- Replace ambiguous nouns such as thing, aspect, issue, solution, data, and system with specific referents.
- Check sentence scope so modifiers and exceptions attach to the intended clause.
- Check whether passive voice hides responsibility.
- Check whether nominalization hides action or causality.
- Check whether long sentences combine independent claims that need separate support.
- Check whether dense terminology imposes avoidable cognitive load.
- Check whether tone fits the audience and stakes without weakening precision.
- Check whether rhetorical confidence exceeds evidentiary confidence.
- Check spelling or grammar only when it changes meaning, credibility, or comprehension.

## 15. Examples, Visuals, Tables, and Code Excerpts

- Check that every example instantiates the stated rule rather than an unstated special case.
- Check that examples cover a representative normal case and decisive boundary cases.
- Check that examples do not introduce undefined terms or hidden assumptions.
- Check that examples and counterexamples are clearly labeled.
- Check that sample values use correct units, types, and realistic ranges.
- Check that examples remain consistent with current interfaces and terminology.
- Check that diagrams have a stated purpose and readable labels.
- Check that arrows have defined direction and semantics.
- Check that shapes, colors, line styles, and grouping have legends when meaning is not standard.
- Check that diagrams distinguish control, data, dependency, ownership, and chronology.
- Check that diagrams do not omit a component essential to the stated behavior.
- Check that tables have meaningful headers, units, sources, and consistent granularity.
- Check that table rows and columns are mutually comparable.
- Check that empty cells, dashes, zeros, and unavailable values are distinguishable.
- Check that figures identify scale, baseline, uncertainty, and data source.
- Check that color is not the only carrier of meaning.
- Check that visual ordering matches reading order and narrative order.
- Check that screenshots and mockups do not masquerade as implemented behavior.
- Check that pseudocode states its abstraction limits.
- Check that code excerpts compile or are explicitly marked illustrative.
- Check that elided code does not hide behavior decisive to the claim.
- Check that copied output identifies environment and reproducibility conditions.

## 16. Integrity, Safety, Security, Privacy, and Accessibility

- Check whether the artifact creates foreseeable harm, misuse, exclusion, or deception.
- Check whether affected stakeholders are represented in the assumptions and tradeoffs.
- Check whether consent, notice, recourse, and accountability are needed.
- Check whether incentives encourage manipulation or metric gaming.
- Check whether conflicts of interest are disclosed.
- Check whether authorship, source use, and contribution claims are accurate.
- Check whether confidential or personal information is necessary and minimized.
- Check data purpose, collection, access, retention, sharing, deletion, and secondary use.
- Check authentication, authorization, least privilege, and separation of duties.
- Check trust boundaries, attacker capabilities, abuse cases, and threat assumptions.
- Check input validation, output encoding, secret handling, logging, and error disclosure.
- Check dependency and supply-chain trust.
- Check secure defaults and failure behavior.
- Check whether auditability conflicts with privacy and how that tradeoff is resolved.
- Check compliance claims against named obligations rather than vague assurances.
- Check whether human override or appeal is required for consequential decisions.
- Check whether automation bias and false confidence are mitigated.
- Check keyboard, screen-reader, contrast, motion, language, cognitive, and assistive-technology needs when applicable.
- Check whether accessibility is part of acceptance rather than deferred polish.
- Check whether safety controls are testable and monitored.
- Check whether incident response, containment, recovery, and notification responsibilities are defined.
- Do not claim legal, ethical, secure, private, safe, or accessible status without criteria and evidence.

## 17. Academic and Research Lens

- Require a precise research question, thesis, or hypothesis.
- Check novelty claims against the stated literature boundary.
- Check that the literature review synthesizes positions rather than listing sources.
- Check that cited literature includes relevant contrary findings and recent work.
- Check whether the theoretical framework defines constructs and relationships.
- Check construct validity, internal validity, external validity, and conclusion validity.
- Check that method follows from the research question.
- Check population, sampling, recruitment, inclusion, exclusion, and attrition.
- Check controls, randomization, blinding, intervention fidelity, and contamination where applicable.
- Check instrument validity, reliability, calibration, and administration.
- Check qualitative sampling, saturation, coding, reflexivity, triangulation, and negative cases where applicable.
- Check preregistration, protocol deviations, and post hoc analyses.
- Check data availability, code availability, materials, and reproducibility.
- Check ethics approval, consent, risk, privacy, and vulnerable populations.
- Check whether results are separated from interpretation.
- Check whether the discussion returns to the research question.
- Check whether limitations identify direction and likely magnitude of bias when possible.
- Check whether generalization remains within the studied population and setting.
- Check whether null results are interpreted without proving equivalence.
- Check whether replication, robustness, and sensitivity are addressed.
- Check whether abstract and conclusion preserve methodological caveats.
- Check whether future work follows from actual limitations rather than generic filler.
- Check whether claims of proof, discovery, causality, and significance match the design.
- Require a defensible answer to the strongest seminar objection.

## 18. Technical Architecture and Design Lens

- Identify system boundary, actors, external dependencies, and trust boundaries.
- Check that requirements drive architecture rather than preferred technology.
- Check separation of concerns and ownership boundaries.
- Check that static facts, runtime behavior, policy, transport, persistence, and presentation live in appropriate layers.
- Check public interfaces, inputs, outputs, invariants, preconditions, postconditions, and error semantics.
- Check data model identity, lifecycle, cardinality, uniqueness, nullability, and versioning.
- Check state ownership, concurrency, consistency, and transaction semantics.
- Check dependency direction, cycles, and initialization order.
- Check failure isolation, retries, idempotency, timeout, cancellation, and backpressure.
- Check authentication, authorization, validation, trust boundaries, and secret handling.
- Check performance complexity on expected and worst-case paths.
- Check memory, storage, network, and compute growth.
- Check cache consistency and invalidation.
- Check observability and diagnosability at component boundaries.
- Check configuration precedence, defaults, validation, and reload behavior.
- Check API and schema compatibility, evolution, and deprecation.
- Check migration, mixed-version operation, rollback, and irreversible writes.
- Check build-versus-buy assumptions and dependency lifecycle.
- Check test seams, deterministic behavior, fixtures, and acceptance evidence.
- Check whether extension points preserve core invariants and avoid one-off branches.
- Check whether abstraction removes real complexity rather than hiding it.
- Check whether a proposed generalization has at least one credible future consumer.
- Check whether implementation shortcuts silently weaken correctness or soundness.
- Check whether diagrams, prose, and interface definitions describe the same architecture.
- Check whether operational ownership is part of the design.

## 19. Plans, Specifications, and Requirements Lens

- Require a concrete desired outcome and observable completion criteria.
- Check that the current state and motivating problem are evidenced.
- Check that the plan is decision-complete for the implementer.
- Check that no step relies on an unnamed choice, owner, interface, or policy.
- Check sequencing and prerequisite refactors before feature layering.
- Check whether shared mechanisms should be generalized before narrow implementation.
- Check that public API, schema, configuration, behavior, and compatibility changes are explicit.
- Check normal behavior, validation, defaults, errors, and edge cases.
- Check data flow and state transitions across subsystem boundaries.
- Check performance, security, accessibility, and operational requirements.
- Check migration, rollout, monitoring, rollback, and cleanup.
- Check test cases against desired behavior rather than current implementation.
- Check acceptance criteria for independence, observability, and completeness.
- Check whether assumptions are explicit and falsifiable.
- Check whether non-goals prevent scope creep without hiding prerequisites.
- Check whether future extensions are reserved through stable boundaries rather than speculative implementation.
- Check whether each task produces an artifact or verified behavior needed by a later task.
- Check whether risks have mitigations and decision triggers.
- Check whether documentation and consumer adoption are included.
- Check whether the plan can be executed without rediscovering material decisions.
- Reject chronological task lists that omit design intent and behavioral contracts.

## 20. Code Explanation and API Documentation Lens

- Check the explanation against the actual code, interface, or authoritative source.
- Identify entry points, inputs, outputs, side effects, ownership, and lifecycle.
- Explain invariants and non-obvious rationale rather than narrating syntax.
- Check that control flow and data flow descriptions match execution.
- Check whether errors, panics, exceptions, retries, and cancellation are covered.
- Check concurrency, ordering, mutability, aliasing, and resource lifetime when relevant.
- Check complexity and performance claims against the algorithm.
- Check security and validation assumptions at boundaries.
- Check examples against current signatures and types.
- Check whether omitted setup makes examples non-runnable.
- Check whether API terms such as optional, required, idempotent, thread-safe, stable, and deprecated have exact semantics.
- Check default values and precedence rules.
- Check version availability, feature flags, platform differences, and compatibility.
- Check whether return values and error variants are complete.
- Check whether examples demonstrate decisive edge behavior, not only happy paths.
- Check whether implementation detail is mistakenly promised as stable API behavior.
- Check whether documentation promises behavior the code does not enforce.
- Check whether caveats are placed at the point of use.
- Check whether links and symbol names resolve.
- Distinguish verified code behavior from inferred intent.

## 21. Presentation and Seminar Lens

- Require a clear seminar question, thesis, or offer in the opening.
- Check that the audience knows why the topic matters without inflated claims.
- Check narrative order: problem, concepts, method or approach, evidence, implications, limitations, and conclusion as applicable.
- Check that each slide or section has one main communicative job.
- Check that slide titles state claims or functions rather than vague topics.
- Check that definitions precede diagrams, results, and objections that use them.
- Check that visuals are readable at presentation distance.
- Check that text density, chart complexity, and pacing fit available time.
- Check that spoken explanation is not required to repair an incoherent slide.
- Check that speaker claims match displayed evidence.
- Check that transitions preserve the argumentative thread.
- Check that demonstrations have setup, failure fallback, and time bounds.
- Check that essential evidence is not hidden in backup material.
- Check that citations remain recoverable without dominating slides.
- Check that the conclusion answers the opening question.
- Check that limitations appear before audience questions expose them.
- Anticipate questions about definitions, assumptions, method, evidence, alternatives, generalization, and consequences.
- Require concise answers that do not overclaim beyond the artifact.
- Check that accessibility includes contrast, readable type, non-color encoding, captions, and described visuals.
- Check that the presentation can be shortened without losing the central proof path.

## 22. Procedures and Instructional Material Lens

- Identify the intended operator, prerequisite knowledge, authority, environment, and tools.
- State prerequisites before irreversible or dependent steps.
- Check that steps are ordered by actual dependency.
- Check that each action has an observable expected result.
- Check decision points and branch conditions.
- Check commands, paths, names, versions, and placeholders for exactness.
- Check whether examples distinguish literal text from values to substitute.
- Check permissions and safety constraints before privileged actions.
- Check backups, previews, dry runs, and recovery before destructive actions.
- Check whether stopping conditions and success criteria are explicit.
- Check failure symptoms, diagnosis, retry, escalation, and rollback.
- Check whether rerunning steps is safe.
- Check whether partial completion leaves a recoverable state.
- Check platform, version, locale, and environment assumptions.
- Check whether prerequisite output is reused consistently in later steps.
- Check whether warnings appear before the relevant hazard.
- Check whether verification tests the intended outcome rather than only command completion.
- Check whether cleanup removes only artifacts created by the procedure.
- Check whether future changes can update one authoritative procedure rather than duplicated copies.

## 23. Data Analysis and Results Lens

- Identify the question, target variable, unit of analysis, population, and decision context.
- Check data provenance, collection conditions, schema, and version.
- Check data cleaning, exclusions, transformations, joins, and deduplication.
- Check missingness mechanism and handling.
- Check leakage between outcome, features, and evaluation data.
- Check exploratory and confirmatory analyses are distinguished.
- Check metric definitions and denominators.
- Check uncertainty, sensitivity, and robustness.
- Check subgroup analysis for sample size, multiplicity, and fairness.
- Check model selection, tuning, calibration, validation, and drift.
- Check whether explanatory claims exceed predictive evidence.
- Check whether visualizations reveal rather than hide distribution and uncertainty.
- Check whether anomalous results are investigated consistently.
- Check whether negative and null results are retained.
- Check reproducible code, environment, seeds, and data access.
- Check whether conclusions remain valid under alternate reasonable preprocessing choices.
- Check whether decision thresholds reflect asymmetric costs.
- Check monitoring for data quality and post-deployment performance where applicable.

## 24. Policy, Strategy, and Business Case Lens

- Identify the decision maker, beneficiaries, affected parties, and implementation authority.
- Check that the problem definition is evidenced and not tailored to a preferred solution.
- Check incentives, strategic alignment, and organizational constraints.
- Check market, regulatory, contractual, and competitive assumptions.
- Check demand, adoption, pricing, cost, revenue, and capacity assumptions.
- Check total cost across acquisition, integration, operation, support, migration, and exit.
- Check whether benefits are incremental, attributable, and time-bounded.
- Check scenario, sensitivity, break-even, and downside analysis.
- Check distribution of costs, benefits, and risks across stakeholders.
- Check governance, accountability, measurement, and review cadence.
- Check unintended behavior, gaming, displacement, and second-order effects.
- Check pilot design and criteria for expansion, revision, or termination.
- Check legal, ethical, privacy, accessibility, and reputational implications.
- Check vendor lock-in, concentration risk, and exit rights.
- Check whether success metrics encourage the actual objective.
- Check whether policy exceptions have criteria and oversight.
- Check whether the recommendation remains coherent if key forecasts fail.

## 25. False-Positive Controls

- Do not infer missing intent when the artifact states it clearly elsewhere.
- Do not require every standard term to be defined for an expert audience.
- Do not accept local redefinition merely because the audience is expert.
- Do not call two statements contradictory until scope, time, modality, and abstraction are aligned.
- Do not call a claim false solely because its evidence is absent from the artifact.
- Do not treat a plausible alternative as proof that the chosen approach is defective.
- Do not require alternatives that cannot satisfy binding constraints.
- Do not reject a tradeoff because another value could reasonably be prioritized.
- Do not treat intentional approximation as error when its bounds and consequences are sound.
- Do not demand precision unsupported by available measurement.
- Do not demand implementation detail from a conceptual artifact unless adoption depends on it.
- Do not excuse missing behavioral contracts merely because the artifact is called conceptual.
- Do not demand edge-case machinery that contradicts declared scope; require a safe boundary instead.
- Do not mistake concise writing for incomplete reasoning when dependencies remain explicit.
- Do not mistake long writing for complete reasoning.
- Do not report grammar, formatting, or taste as substantive defects without a consequence.
- Do not repeat one root issue as separate findings for every symptom.
- Do not combine unrelated defects into one vague finding.
- Do not cite an entire artifact when an exact locator is available.
- Do not prescribe a rewrite before identifying what must change and why.
- Do not silently replace the author's defensible objective with a preferred one.
- Do not invent authorities, requirements, facts, data, quotations, citations, or tool results.
- Do not conceal verification limits behind confident language.
- Do not praise away unresolved defects.
- Do not imply completeness beyond the reviewed scope and evidence.

## 26. Final Acceptance Audit

- Confirm that the verdict follows from the highest-severity unresolved finding.
- Confirm that no critical or major finding is buried under optional refinements.
- Confirm that every finding has a precise locator and observable evidence.
- Confirm that every confirmed defect states a violated principle and material consequence.
- Confirm that every probable risk explains what missing context could change the judgment.
- Confirm that every open question can change a conclusion, severity, or repair.
- Confirm that every repair preserves defensible intent and addresses the root cause.
- Confirm that every verification method could distinguish repaired from unrepaired behavior.
- Confirm that severity reflects impact rather than reviewer preference.
- Confirm that confidence reflects evidence rather than rhetorical certainty.
- Confirm that duplicate and derivative findings are consolidated.
- Confirm that inaccessible sources and unperformed checks are disclosed.
- Confirm that repaired passages introduce no new undefined concepts or contradictions.
- Confirm that future extension remains possible at stable, explicit boundaries.
- Confirm that an acceptable verdict is limited to the reviewed scope.
- Confirm that the final response itself satisfies this checklist before delivery.
