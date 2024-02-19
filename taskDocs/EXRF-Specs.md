# EXRF - Expense Report Format - version 0.0.1

## Introduction

The EXRF format is a new, **never seen before** file format for expense reports. It is a simple text-based format that is easy to parse and understand.

The format is designed to be human-readable and easy to edit, but it is also easy to parse and process by machines.

## Specification

The EXRF format is a text-based format with the `.exrf` file extension.
The EXRF format is a schemaless format, meaning that it does not have a fixed schema, and can be shaped as you wish by following the structure described below.

### General structure

The EXRF file is a line-based textual file. By itself, the EXRF format doesn't support data-types other than text, that means that all values are strings.  
Later in this document, you will learn about fields ands structures, but in general every value in the EXRF format is a string.

This design is intentional, it allows the EXRF format to be simple and flexible, every implementation can handle the parsing and validation of the values as it sees fit.

For example, one can use the EXRF format to represent a monetary value with a pre-defined rule for parsing and validation, for example, the value:

```exrf
100,00USD
```

is simply a string of `"100,00USD"`, but it can be parsed and validated by the application as a monetary value. The freedom to define the rules for parsing and validation is left to the application.

---

## The Building Blocks

The EXRF format supports only 3 structures: `field`, `block`, and `list`. Each of these building blocks is described below.

### Field

A field is a single key-value pair, represented in a single line in the EXRF file.
Fields cannot wrap to the next line, they must be in a single line.

Fields are defined as follows: `<key>::<value>`.

For example, here's an EXRF file with some fields:

```exrf
name::John Doe
age::25
email::john@example.com
is_active::true
```

This EXRF [block](#block) contains the following fields: `name`, `age`, `email`, and `is_active` with their respective values. Remeber that values are always string, here's a JSON equivalent:

```json
{
  "name": "John Doe",
  "age": "25",
  "email": "john@example.com",
  "is_active": "true"
}
```

Fields can be declared in any order, and they can be anywhere in the file.

There is no limit to the number of fields in an EXRF file, you can have as many as you want.

The keys and values can be anything, include spaces, special characters, and even emojis as long as they are valid UTF-8 characters, and do not conflict with the EXRF syntax (see limitations below).

```exrf
🔥::This is lit!
User::John Doe
Last Seen!!::Yesterday
```

as JSON:

```json
{
  "🔥": "This is lit!",
  "User": "John Doe",
  "Last Seen!!": "Yesterday"
}
```

#### Field Limitations

1. Keys cannot contain following characters `:`,`[`,`]`. They are reserved for other structural definitions.
2. Spaces around the `::` seperator are **not ignored** and considered part of the key or value.  
   For example, the following field:

   ```exrf
   name :: John Doe
   ```

   is not the same as:

   ```exrf
   name::John Doe
   ```

   The first field has a key of `"name "` (with a space at the end) and a value of `" John Doe"` (with a space at the beginning).

---

### Block

A block is a named collection of fields, blocks, and [lists](#list). Blocks are scoped and can be nested inside other blocks.

In general blocks act like objects in JSON.

In the EXRF format, blocks have opening and closing annotations, which occupy a single line each. To open a block use the following syntaxt `:<block-name>:`, and to close a block use the following syntax `::<block-name>::`.

```exrf
:person:
::person::
```

This EXRF example shows a block named `person` with no fields inside it.
Here's a JSON equivalent:

```json
{
  "person": {}
}
```

Blocks are used to group other structures, here's an example of a block with some fields:

```exrf
:person:
name::John Doe
age::25
email::john@example.com
::person::
```

This example contains a named block: `person` with 3 fields inside it: `name`, `age`, and `email`. Here's a JSON equivalent:

```json
{
  "person": {
    "name": "John Doe",
    "age": "25",
    "email": "john@example.com"
  }
}
```

Entries inside blocks are not ordered, that means that the following EXRF:

```exrf
:person:
name::John Doe
age::25
::person::
```

is the same as:

```exrf
:person:
age::25
name::John Doe
::person::
```

#### Nested Blocks

Blocks can be declared inside other blocks, as long as they are properly opened and closed. Here's an example of a block with another block inside it:

```exrf
:person:
name::John Doe
age::25
:addres:
street::123 Main St.
city::New York
::address::
::person::
```

JSON equivalent:

```json
{
  "person": {
    "name": "John Doe",
    "age": "25",
    "address": {
      "street": "123 Main St.",
      "city": "New York"
    }
  }
}
```

Block names can be anything, include spaces, special characters, and even emojis as long as they are valid UTF-8 characters, and do not conflict with the EXRF syntax (see limitations below).

```exrf
:🔥:
name::John Doe
::🔥::
```

#### EXRF File is a Block

Every EXRF file is considered a `block` with no name, and it can contain any number of fields, blocks, and lists.

For example, the empty file `test.exrf`:

```exrf

```

is an empty block with no values inside,  
here's a JSON equivalent of the above EXRF file, `test.json`:

```json
{}
```

The following file `test2.exrf`:

```exrf
name::John Doe
age::25
```

Is a block with 2 fields inside it, here's a JSON equivalent of the above EXRF file, `test2.json`:

```json
{
  "name": "John Doe",
  "age": "25"
}
```

#### Block Limitations

1. Block names follow the same rules as field keys, they cannot contain the following characters `:`,`[`,`]`. They are reserved for the syntax.
2. Spaces around the block name are **not ignored** and considered part of the block name.  
   For example, the following block:

   ```exrf
   : person :
   ```

   is not the same as:

   ```exrf
   :person:
   ```

   The first block has a name of `" person "` (with a space at the beginning and end).

---

### List

A list is a named collection that contains multiple nameless blocks, it means that the blocks inside a list do not have a name/key, they are like items in an array.

Lists have opening and closing annotations, and are declared using the following syntaxt:

- to open a list : `[<list-name>]`
- to close a list : `[[<list-name>]]`

Here's an example of an empty list:

```exrf
[expenses]
[[expenses]]
```

is equivalent to the following JSON:

```json
{
  "expenses": []
}
```

Here's an example of a list with one block inside it:

```exrf

[expenses]
amount::100,00USD
[[expenses]]
```

This is equivalent to the following JSON:

```json
{
  "expenses": [{ "amount": "100,00USD" }]
}
```

In order to make a list "list", it has to be able to contain multiple blocks.

For that we're using the `::::` keyword to separate the blocks inside a list.

```exrf
[expenses]
amount::100,00USD
::::
amount::200,00USD
::::
amount::300,00USD
[[expenses]]
```

is equivalent to the following JSON:

```json
{
  "expenses": [
    { "amount": "100,00USD" },
    { "amount": "200,00USD" },
    { "amount": "300,00USD" }
  ]
}
```

The blocks inside a list can be of any shape, and also include other lists and blocks inside them.

```exrf
[items]
name::Item 1
::::
name::Item 2
value::100,00USD
::::
name::Item 3
:error_details:
code::100
message::Item is not available
::error_details::
::::
name::Item 4
[reviewers]
name::John Doe
::::
name::Jane Doe
[[reviewers]]
[[items]]
```

is equivalent to the following JSON:

```json
{
  "items": [
    { "name": "Item 1" },
    { "name": "Item 2", "value": "100,00USD" },
    {
      "name": "Item 3",
      "error_details": {
        "code": "100",
        "message": "Item is not available"
      }
    },
    {
      "name": "Item 4",
      "reviewers": [{ "name": "John Doe" }, { "name": "Jane Doe" }]
    }
  ]
}
```

#### List Limitations

1. List names follow the same rules as block and field names, they cannot contain the following characters `:`,`[`,`]`. They are reserved for the syntax.

2. Spaces around the list name are **not ignored** and considered part of the list name.  
   For example, the following list:

   ```exrf
   [ expenses ]
   [[ expenses ]]
   ```

   is not the same as:

   ```exrf
   [expenses]
   [[expenses]]
   ```

   The first list has a name of `" expenses "` (with a space at the beginning and end).

3. Note that `::::` seperators create a new block, if no fields are declared inside the block, it will be an empty block.

   For example, the following EXRF:

   ```exrf
   [items]
   ::::
   ::::
   [[items]]
   ```

   is equivalent to the following JSON:

   ```json
   {
     "items": [{}, {}, {}]
   }
   ```
