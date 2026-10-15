# Unpublished issue-citation correction — #367

The final publication review caught two local commits without their owning issue
references. Both messages are corrected and signed, preserving original authors
and identical tree objects. Their original graph remains on the retained local
feature/m7-pre-citation-20261015 branch; historical evidence IDs remain readable.
No published commit was rewritten and no force-push occurred. The mapping records
both IDs and identical source trees. Subsequent push runs normal hooks.

The existing next-only issue-coverage check must run after local integration,
not only before the last commit. This repeats the previously recorded omission;
check the final pending messages as well as the integrated gate. No product
source, fixture expectation or audit completion state changed.
