from setuptools import setup

APP = ["pdf_page_duplicator_gui.py"]
OPTIONS = {
    "argv_emulation": False,
    "packages": ["pypdf"],
    "plist": {
        "CFBundleName": "PDF Page Duplicator",
        "CFBundleDisplayName": "PDF Page Duplicator",
        "CFBundleIdentifier": "com.local.pdfpageduplicator",
        "CFBundleShortVersionString": "1.0.0",
        "CFBundleVersion": "1",
    },
}

setup(
    app=APP,
    options={"py2app": OPTIONS},
    setup_requires=["py2app"],
)
