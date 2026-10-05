# Final reply to Reviewer 1, Comment D3

We thank the reviewer for these suggestions. We agree that all three works are
relevant to our setting, and we will incorporate them into the related-work
discussion with their specific relationship to our contribution stated
explicitly, rather than adding them as isolated citations.

Oort~[3] is the closest to one of the mechanisms we isolate. Oort improves
federated training through guided participant selection, explicitly trading off
each participant's utility against system efficiency. DirBridge addresses a
different, complementary aspect of the same underlying phenomenon: even when
participant selection or buffered execution is efficient, the set of clients
that returns first may still overrepresent fast direction groups. Oort shapes
\emph{which} clients participate; DirBridge corrects the \emph{population
composition} of whatever update stream the system actually observes, and does so
without controlling or reordering participation. We will cite Oort when
discussing selection-side approaches to heterogeneity and position DirBridge as
addressing representation bias that persists under a given (uncontrolled)
arrival process.

FS-Real~[1] provides a real-world cross-device federated learning platform whose
measurements document that availability, latency, and participation patterns in
practical deployments are far from uniform. We will cite it in two places: as
empirical motivation that first-arriving updates form a systematically biased
sample of the client population, which is precisely the phenomenon DirBridge is
designed to correct; and as a platform-level reference supporting the realism of
our deployment-oriented experiments (e.g., the trace-based evaluation added in
the revision, where real network traces produce the same representation-bias
effect under controlled data conditions).

BTFL~[2] addresses test-time generalization under internal and external
distribution shifts in federated learning. Its concern is distributional
robustness of the learned model at inference time, which is orthogonal to the
composition-of-arrivals problem we study: BTFL corrects how the model behaves
under shifted input distributions, whereas DirBridge corrects which population
directions the training update represents. We will cite BTFL in the revised
related-work section to delineate this boundary---test-time adaptation and
direction-level correction of the training stream address different stages of
the same system-heterogeneity landscape.

In summary, the three references strengthen the related-work positioning along
three complementary axes---real-world deployment evidence [1], selection-side
mitigation [3], and inference-time robustness [2]---each of which clarifies, by
contrast, that DirBridge's contribution is a training-time, aggregation-side
correction of direction-level representation bias. The revised manuscript
incorporates all three with these relationships made explicit.
