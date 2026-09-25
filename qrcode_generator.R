library(qrcode)
# Generate a QR code for a URL
code <- qr_code("https://www.r-project.org")
# Print the QR code in the console
print(code)
# Generate and save as SVG
generate_svg(code, filename = "r-logo.svg")