module day04


function a(data)
    num_in_common = [
        length(intersect(winning, owned))
        for (winning, owned) in data
    ]
    return sum(
        2^(num_winning-1)
        for num_winning in num_in_common
        if num_winning > 0
    )
end

function b(data)
    num_in_common = [
        length(intersect(winning, owned))
        for (winning, owned) in data
    ]
    num_copies = ones(Int, length(data))
    for (i, num_winning) in enumerate(num_in_common)
        if num_winning >= 1
            num_copies[i+1:min(i+num_winning, length(data))] .+= num_copies[i]
        end
    end

    return sum(num_copies)
end


function parse_card(line)
    winning_numbers, owned_numbers = map(Set, map(split, split(split(line, ": ")[2], "|")))
    return winning_numbers, owned_numbers
end


function parse_file(path)
    lines = readlines(joinpath(@__DIR__, path))
    return [
        parse_card(line)
        for line in lines
    ]
end


function both()
    data = parse_file("../inputs/input04.txt")
    println(a(data))
    println(b(data))
end

end
