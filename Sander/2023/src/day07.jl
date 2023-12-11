module day07


struct CamelCardHand
    cards::String
    bid::Int
    function CamelCardHand(cards::AbstractString, bid::AbstractString)
        new(cards, parse(Int, bid))
    end
end


@enum HAND begin
    high_card = 1
    one_pair = 2
    two_pair = 3
    three_of_a_kind = 4
    full_house = 5
    four_of_a_kind = 6
    five_of_a_kind = 7
end


function determine_hand(hand)
    unique_cards = Set(hand.cards)
    num_unique = length(unique_cards)
    if num_unique == 5
        return high_card
    elseif num_unique == 1
        return five_of_a_kind
    end

    counts = Dict((char, 0) for char in unique_cards)
    for char in hand.cards
        counts[char] += 1
    end
    max_count = maximum(values(counts))
    if max_count == 4
        return four_of_a_kind
    elseif max_count == 3 
        if num_unique == 2 # full_house
            return full_house
        else
            return three_of_a_kind
        end
    elseif max_count == 2
        if num_unique == 3 # two pair 
            return two_pair
        else
            return one_pair
        end
    end
end


function determine_hand_joker(hand)
    unique_cards = Set(hand.cards)
    num_unique = length(unique_cards)
    counts = Dict((char, 0) for char in unique_cards)
    for char in hand.cards
        counts[char] += 1
    end

    num_joker = haskey(counts, 'J') ? counts['J'] : 0
    delete!(counts, 'J')
    if num_joker < 5
        max_count = maximum(values(counts)) + num_joker
    else
        max_count = num_joker
    end

    if max_count == 5
        return five_of_a_kind
    elseif max_count == 4
        return four_of_a_kind
    elseif max_count == 3 
        if ((num_unique == 2 && num_joker == 0)
           || (num_unique == 3 && num_joker == 1)) # full_house
            return full_house
        else
            return three_of_a_kind
        end
    elseif max_count == 2
        if num_unique == 3 # two pair 
            return two_pair
        else
            return one_pair
        end
    elseif max_count == 1
        return high_card
    end
end


"""
    hand_compare(hand, other)

compare two CamelCardHands according to the rules:
better poker hand wins, with ties broken by comparing 1st, 2nd, ... cards
"""
function hand_compare(hand, other)
    h1, h2 = determine_hand(hand), determine_hand(other)
    if h1 != h2
        return h1 < h2
    end

    card_values = Dict(
        'A' => 14, 'K' => 13, 'Q' => 12, 'J' => 11, 'T' => 10,
        '9' => 9, '8' => 8, '7' => 7, '6' => 6,
        '5' => 5, '4' => 4, '3' => 3, '2' => 2,
    )
    for (card1, card2) in zip(hand.cards, other.cards)
        if card1 != card2
            return card_values[card1] < card_values[card2]
        end
    end
end


"""
    hand_compare_joker(hand, other)

compare two CamelCardHands according to the rules:
better poker hand wins, with ties broken by comparing 1st, 2nd, ... cards
includes treating 'J' as jokers instead of jacks
"""
function hand_compare_joker(hand, other)
    h1, h2 = determine_hand_joker(hand), determine_hand_joker(other)
    if h1 != h2
        return h1 < h2
    end

    card_values = Dict(
        'A' => 14, 'K' => 13, 'Q' => 12, 'J' => 1, 'T' => 10,
        '9' => 9, '8' => 8, '7' => 7, '6' => 6,
        '5' => 5, '4' => 4, '3' => 3, '2' => 2,
    )
    for (card1, card2) in zip(hand.cards, other.cards)
        if card1 != card2
            return card_values[card1] < card_values[card2]
        end
    end
end


function a(data)
    sort!(data, lt=hand_compare)
    return sum(
        rank*hand.bid
        for (rank, hand) in enumerate(data)
    )
end


function b(data)
    sort!(data, lt=hand_compare_joker)
    return sum(
        rank*hand.bid
        for (rank, hand) in enumerate(data)
    )
end


function parse_file(path)
    lines = readlines(joinpath(@__DIR__, path))
    return [CamelCardHand(split(line)...) for line in lines]
end


function both()
    data = parse_file("../inputs/input07.txt")
    println(a(data))
    println(b(data))
end

end
