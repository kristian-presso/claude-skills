// Formats dates for the booking confirmation screen.
export function formatBookingDate(d) {
  return d.toLocaleDateString('en-GB', { weekday: 'short', day: 'numeric', month: 'short' });
}
