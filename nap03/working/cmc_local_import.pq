let
    Source = Json.Document(File.Contents("C:\Users\nagya\dev\school\BPA\nap03\working\cmc_power_query\quotes.json")),
    Coins = Record.ToTable(Source[data]),
    Expanded = Table.ExpandRecordColumn(Coins, "Value", {"name", "symbol", "quote"}, {"Név", "Symbol", "quote"}),
    Currency = Table.ExpandRecordColumn(Expanded, "quote", {"EUR"}, {"EUR"}),
    Quotes = Table.ExpandRecordColumn(Currency, "EUR", {"price", "percent_change_24h"}, {"Ár (EUR)", "24h változás"}),
    Renamed = Table.RenameColumns(Quotes, {{"Name", "CMC_ID"}}),
    Typed = Table.TransformColumnTypes(Renamed, {{"CMC_ID", Int64.Type}, {"Név", type text}, {"Symbol", type text}, {"Ár (EUR)", type number}, {"24h változás", type number}}),
    Provider = Table.AddColumn(Typed, "ProviderTimestamp", each Source[status][timestamp], type text),
    Result = Table.AddColumn(Provider, "FetchedUTC", each Source[fetched_utc], type text)
in
    Result
