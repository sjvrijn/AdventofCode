using AdventofCode: day07

@testset "Day 7" begin

    @testset "Day 7, part 1" begin
        testfiles = Dict(
            "input07-test1.txt" => 6440,
        )
        for (file, result) in testfiles
            data = day07.parse_file(joinpath(INPUT, file))
            @test day07.a(data) == result
        end
    end

    @testset "Day 7, helpers" begin
        hands = [
            day07.CamelCardHand("32T3K", "0"),
            day07.CamelCardHand("T55J5", "0"),
            day07.CamelCardHand("KK677", "0"),
            day07.CamelCardHand("KTJJT", "0"),
            day07.CamelCardHand("QQQJA", "0"),
        ]
        for hand in hands[2:end]
            @test day07.hand_compare(hands[1], hand)
        end
        @test !day07.hand_compare(hands[3], hands[4])
        @test day07.hand_compare(hands[2], hands[5])
    end

    @testset "Day 7, part 2" begin
        testfiles = Dict(
            "input07-test1.txt" => 5905,
        )
        for (file, result) in testfiles
            data = day07.parse_file(joinpath(INPUT, file))
            @test day07.b(data) == result
        end
    end

end