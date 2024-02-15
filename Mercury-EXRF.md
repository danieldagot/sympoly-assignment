# Mercury EXRF Specification

## Introduction

This document describes the EXRF implementation for "Mercury Invoices".  
It's an extension to the base [EXRF Specification](./EXRF-Specs.md), and it's designed to be used as a standard format for exchanging invoice data between our systems.

**Note**: Before reading this document, it's recommended to read the [EXRF Specification](./EXRF-Specs.md) to understand the basic concepts and structures of the EXRF format.

## General Structure

Mercury's EXRF Extension has a consistent structure that applies to all invoices. Here's the definition of the main blocks and fields that are used in the extension.

### 1. Report

A `Report` is the main block of an invoice.
It contains one field `ID` which is a unique identifier for the invoice and acts like a string, and multiple blocks that represent different parts of the invoice.

Here's a list of the sections that a `Report` has:

- [`Details`](#2-details)
- [`Reporter`](#3-reporter)
- [`Approvers`](#4-approvers)
- [`Transactions`](#5-transactions)

---

### 2. Details

The `Details` section contains the basic information about the invoice.

It has 2 fields `CreatedAt` and `Status`

- `CreatedAt` - is a field that represents the date when the invoice was created. (See [Date](#date))

- `Status` - a number that represents the status of the invoice. It can have one of the following values:
  - `0` - Draft
  - `1` - Submitted
  - `2` - Approved
  - `3` - Rejected

---

### 3. Reporter

`Reporter` is a block that contains the information about the person who created the invoice, it has the shape of a [Person](#person) block.

---

### 4. Approvers

`Approvers` is a list of blocks that contain the information about the people who approved the invoice, each block in the list has the shape of a [Person](#person) block.

---

### 5. Transactions

`Transactions` is a list of blocks that contain the information about the transactions in the invoice.

Each block in the list has the following fields:

- `Data` - A field that contains [Transaction Data](#transaction-data)
- `Reference` - A 16-letters long string that represents the reference of the transaction, it contains only digits and uppercase letters.
- `Details` - A simple string that represents the details of the transaction.

---

## Custom Encoding

Mercury's EXRF Extension uses a custom encoding for some of the fields. Below we describe the custom encoding for the fields that require it.

---

### Date

A `Date` is a string that represents a date object in the format `YYYYMMDDhhmmss`
- `YYYY` - Year
- `MM` - Month
- `DD` - Day
- `hh` - Hour
- `mm` - Minute
- `ss` - Second

Here's an example of a date string: `20201225123055`
Which represents the date `2020-12-25 12:30:55`

---

### Person

A `Person` is a block type that contains the information about an employee or a person in general.

It has 2 fields:

- `FullName` - The full name of the person.
- `Email` - The email of the person.

---

### Amount

An `Amount` is a number that represents a monetary value.

It contains the following parts:

1. Integer part - The whole number part of the amount.
2. Decimal part - The decimal part of the amount.

The decimal part is always 2 digits long. If the amount has no decimal part, it's represented as `00`.

The integer part has no specific length, it can be any length.

The parts are separated by a comma `,`.

Examples:

- `123456,78`
- `1,34`
- `1000000,00`
- `0,00`

#### Note

- Amounts are always positive, there is no sign for the amount, the sign is determined by the `Type` field in the [Transaction Data](#transaction-data).
- The integer part cannot have any leading zeros, and the decimal part cannot have any trailing zeros.

---

### Currency

A `Currency` is a string that represents a currency code.

The currency data type follows the [ISO 4217](https://en.wikipedia.org/wiki/ISO_4217) standard.

Examples:

- `USD`
- `EUR`
- `GBP`

---

### Transaction Data

`Transaction Data` is a field that stores encoded data about the transaction.

The transaction data is composed of 4 parts:

1. `Date` - (See [Date](#date))
2. `Type` - Credit or Debit, a constant char (`"C" | "D"`)
3. `Amount` - (See [Amount](#amount))
4. `Currency` - (See [Currency](#currency))

The parts are not separated by any character, they are just concatenated together, this is the format of the transaction data:  
`{Date}{Type}{Amount}{Currency}`

Example of a transaction data: `20201225123055C120558,78USD`

This is the breakdown of the transaction data:

- `Date` - `20201225123055` - `2020-12-25 12:30:55`
- `Type` - `C` - Credit
- `Amount` - `120558,78` - 120558.78
- `Currency` - `USD` - US Dollar

---

## Example Invoice

This is an example of a valid Mercury's EXRF Extension invoice:

```exrf
:Report:
ID::44qsNRSD5LBP

:Details:
CraetedAt::20231004220721
Status::1
::Details::

:Reporter:
FullName::Sammy Rempel
Email::Camren.Beatty28@gmail.com
::Reporter::

[Approvers]
FullName::Marguerite White
Email::Demetris.Kihn33@yahoo.com
::::
FullName::Blake Wyman
Email::Travis.Reichert36@yahoo.com
[[Approvers]]

[Transactions]
Data::20230801101753C76254,74TRY
Reference::3ZW0Y9RMWXGY3R6H
Details::deposit for Koch - Howell paid by card ***(...1893)
::::
Data::20240119233344C55901,52RWF
Reference::CVINYYMFNA2VWEW3
Details::withdrawal for Schinner, Ruecker and Grady paid by card ***(...0459)
::::
Data::20230616170750D86042,75KES
Reference::PVEIL6ZRLZDYXNAS
Details::invoice for Rodriguez - Bechtelar paid by card ***(...8523)
[[Transactions]]
::Report::
```
