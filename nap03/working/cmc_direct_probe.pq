let
    EnvText = Text.FromBinary(File.Contents("C:\Users\nagya\dev\school\BPA\.env.local"), TextEncoding.Utf8),
    EnvLines = Lines.FromText(EnvText),
    KeyLines = List.Select(EnvLines, each Text.Contains(_, "=") and Text.Trim(Text.BeforeDelimiter(_, "="), {Character.FromNumber(65279), " ", "#(tab)"}) = "CMC_PRO_API_KEY"),
    RawKey = if List.Count(KeyLines) = 1 then Text.Trim(Text.AfterDelimiter(KeyLines{0}, "=")) else error "Expected exactly one CMC key entry in the root credential store.",
    Quote = Character.FromNumber(34),
    Key = if (Text.StartsWith(RawKey, Quote) and Text.EndsWith(RawKey, Quote)) or (Text.StartsWith(RawKey, "'") and Text.EndsWith(RawKey, "'")) then Text.Middle(RawKey, 1, Text.Length(RawKey) - 2) else RawKey,
    Response = if Text.Length(Key) > 0 then Web.Contents("https://pro-api.coinmarketcap.com", [RelativePath="v1/cryptocurrency/quotes/latest", Query=[id="1,1027", convert="EUR"], Headers=[#"X-CMC_PRO_API_KEY"=Key, Accept="application/json"], IsRetry=true, ManualStatusHandling={300,301,302,303,307,308}, Timeout=#duration(0,0,0,30)]) else error "CMC key is empty.",
    HttpStatus = Record.FieldOrDefault(Value.Metadata(Response), "Response.Status", 200),
    Root = if HttpStatus = 200 then Json.Document(Response) else error "Unexpected HTTP response; redirects are not followed.",
    Verified = if Root[status][error_code] = 0 then Root else error "CMC rejected the request.",
    Result = #table({"Connection", "Coins", "ProviderTimestamp"}, {{"Power Query direct", Record.FieldCount(Verified[data]), Verified[status][timestamp]}})
in
    Result
