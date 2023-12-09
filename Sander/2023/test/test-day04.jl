using AdventofCode: day04

@testset "Day 4" begin

    @testset "Day 4, part 1" begin
        testfiles = Dict(
            "input04-test1.txt" => 13,
        )
        for (file, result) in testfiles
            data = day04.parse_file(joinpath(INPUT, file))
            @test day04.a(data) == result
        end
    end

    @testset "Day 4, part 2" begin
        testfiles = Dict(
            "input04-test1.txt" => 30,
        )
        for (file, result) in testfiles
            data = day04.parse_file(joinpath(INPUT, file))
            @test day04.b(data) == result
        end
    end

end