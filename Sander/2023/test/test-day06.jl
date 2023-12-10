using AdventofCode: day06

@testset "Day 6" begin

    @testset "Day 6, part 1" begin
        testfiles = Dict(
            "input06-test1.txt" => 288,
        )
        for (file, result) in testfiles
            data = day06.parse_file(joinpath(INPUT, file))
            @test day06.a(data) == result
        end
    end

    @testset "Day 6, part 2" begin
        testfiles = Dict(
            "input06-test1.txt" => 71503,
        )
        for (file, result) in testfiles
            data = day06.parse_file(joinpath(INPUT, file))
            @test day06.b(data) == result
        end
    end

end