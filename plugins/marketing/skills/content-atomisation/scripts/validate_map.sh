#!/usr/bin/env bash
# validate_map.sh - check an atomisation map before anything is drafted or scheduled.
#
# INPUT (stdin or a file argument): TSV, one piece per line, 7 fields:
#   sequence<TAB>lag_days<TAB>channel<TAB>format<TAB>core_claim<TAB>link_target<TAB>cta
# Row with sequence 1 is the hub (the long-form source). Its lag_days is 0 and its
# cta may be "N/A". A header row starting with "sequence" is skipped.
#
# CHECKS
#   1. Exactly one hub row (sequence 1) with lag_days 0.
#   2. At least one derivative (sequence 2 or more).
#   3. Every row has all 7 fields, none empty.
#   4. Sequences are unique and run 1..N with no gaps.
#   5. lag_days is a whole number, and every derivative's lag_days is 1 or more.
#   6. No two rows share the same core_claim (case and spacing ignored).
#   7. Lag days never go backwards as sequence goes up.
#
# OUTPUT
#   stdout: "VALID rows=N derivatives=M span_days=D" on success
#   stderr: one line per problem
#   exit:   0 valid, 1 invalid, 2 usage error
#
# Portable: bash 3.2+ and POSIX awk (works on macOS and Linux). No temp files.
set -uo pipefail

if [ $# -gt 1 ]; then
  echo "usage: validate_map.sh [map.tsv]   (or pipe TSV on stdin)" >&2
  exit 2
fi
if [ $# -eq 1 ] && [ ! -r "$1" ]; then
  echo "error: cannot read $1" >&2
  exit 2
fi

awk -F'\t' '
function trim(s) { gsub(/^[ \t\r]+|[ \t\r]+$/, "", s); return s }
function norm(s) { s = tolower(trim(s)); gsub(/[ \t]+/, " ", s); return s }
/^[ \t\r]*$/ { next }
{
  first = tolower(trim($1))
  if (first == "sequence") next
  rows++
  if (NF != 7) { printf "line %d: expected 7 tab-separated fields, got %d\n", NR, NF > "/dev/stderr"; bad++; next }
  for (i = 1; i <= 7; i++) {
    if (trim($i) == "") { printf "line %d: field %d is empty\n", NR, i > "/dev/stderr"; bad++ }
  }
  seq = trim($1); lag = trim($2)
  if (seq !~ /^[0-9]+$/) { printf "line %d: sequence \"%s\" is not a whole number\n", NR, seq > "/dev/stderr"; bad++; next }
  if (lag !~ /^[0-9]+$/) { printf "line %d: lag_days \"%s\" is not a whole number\n", NR, lag > "/dev/stderr"; bad++; next }
  seq += 0; lag += 0
  if (seq in seen) { printf "line %d: sequence %d appears more than once\n", NR, seq > "/dev/stderr"; bad++ }
  seen[seq] = 1; lagof[seq] = lag
  if (seq > maxseq) maxseq = seq
  if (seq == 1) {
    hubs++
    if (lag != 0) { printf "line %d: hub (sequence 1) must have lag_days 0, got %d\n", NR, lag > "/dev/stderr"; bad++ }
  } else {
    derivs++
    if (lag < 1) { printf "line %d: derivative %d must publish at least 1 day after the hub\n", NR, seq > "/dev/stderr"; bad++ }
  }
  c = norm($5)
  if (c != "" && (c in claim)) { printf "line %d: core_claim duplicates sequence %d\n", NR, claim[c] > "/dev/stderr"; bad++ }
  else claim[c] = seq
  if (lag > span) span = lag
}
END {
  if (rows == 0) { print "error: no rows" > "/dev/stderr"; exit 1 }
  if (hubs == 0) { print "error: no hub row (sequence 1)" > "/dev/stderr"; bad++ }
  if (derivs == 0) { print "error: no derivative rows (sequence 2 or more)" > "/dev/stderr"; bad++ }
  for (s = 1; s <= maxseq; s++) if (!(s in seen)) { printf "error: sequence %d is missing (must run 1..N)\n", s > "/dev/stderr"; bad++ }
  for (s = 2; s <= maxseq; s++) if ((s in seen) && ((s-1) in seen) && lagof[s] < lagof[s-1]) {
    printf "error: sequence %d publishes before sequence %d (lag %d < %d)\n", s, s-1, lagof[s], lagof[s-1] > "/dev/stderr"; bad++
  }
  if (bad > 0) exit 1
  printf "VALID rows=%d derivatives=%d span_days=%d\n", rows, derivs, span
}
' "${1:-/dev/stdin}"
