# ASN labels for Paperless-ngx on Avery labels 

The [recommended workflow](https://docs.paperless-ngx.com/usage/#usage-recommended-workflow) of [Paperless-ngx](https://docs.paperless-ngx.com/) uses QR codes for ASN (archive serial number) labels. This script helps creating them using Python. It outputs a PDF for printing on the label sheets. Make sure to set print size to 100%, not _fit to page_ or similar.

Other Avery (or competitor's) label sizes can be added to `labelInfo` in `AveryLabels.py`. All other settings are configured at the top part of `main.py`.

Use these settings for an initial position test to align your printer:

```python
mode = "text"
debug = True

labelsAlreadyPrinted = 0
labelsCorrupted = 0
labelsToPrint = 1

positionHelper = True
```

# Credits

This is based on the [work from timrprobocom](https://gist.github.com/timrprobocom/3946aca8ab75df8267bbf892a427a1b7)