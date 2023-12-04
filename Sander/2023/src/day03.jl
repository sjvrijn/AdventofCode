module day03

struct PartNumber
    value::Int
    line_number::Int
    offset::UnitRange

    function PartNumber(line_number::Int, match::RegexMatch)
        value = parse(Int, match.match)
        offset = (match.offset-1):(match.offset+length(match.match))
        new(value, line_number, offset)
    end
end

struct Symbol
    symbol::String
    line_number::Int
    offset::Int

    function Symbol(line_number::Int, match::RegexMatch)
        new(match.match, line_number, match.offset)
    end
end

function ispartadjacent(partnumber, symbol)
    if abs(symbol.line_number - partnumber.line_number) > 1
        return false
    elseif !(partnumber.offset.start <= symbol.offset <= partnumber.offset.stop)
        return false
    end
    return true
end

function ispartnumber(partnumber, symbols)
    return any(ispartadjacent(partnumber, symbol) for symbol in symbols)
end


function a(data)
    numbers, symbols = data
    partnumbers = [
        number
        for number in numbers
        if ispartnumber(number, symbols)
    ]
    return sum(part.value for part in partnumbers)
end

function b(data)
    numbers, symbols = data
    gears = Dict(
        symbol => []
        for symbol in symbols
        if symbol.symbol == "*"
    )
    
    for (gear, partnumber) in Iterators.product(keys(gears), numbers)
        if ispartadjacent(partnumber, gear)
            append!(gears[gear], [partnumber])
        end
    end

    return sum(
        parts[1].value * parts[2].value
        for parts in values(gears)
        if length(parts) == 2
    )
end


function parse_file(path)
    lines = readlines(joinpath(@__DIR__, path))

    numbers = [
        PartNumber(line_no, match)
        for (line_no, line) in enumerate(lines)
        for match in eachmatch(r"[0-9]+", line)
    ]

    symbols = [
        Symbol(line_no, match)
        for (line_no, line) in enumerate(lines)
        for match in eachmatch(r"[^0-9\.]+", line)        
    ]

    return numbers, symbols
end


function both()
    data = parse_file("../inputs/input03.txt")
    println(a(data))
    println(b(data))
end

end
